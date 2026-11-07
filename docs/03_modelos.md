# 03 · Modelos, variables y evaluación

## Modelo A — Riesgo financiero dinámico (Behavioral Score)

### Definición
- **Unidad**: cliente-mes.
- **Target**: `1` si el cliente alcanza **90+ días de mora** en cualquier producto en los **12 meses siguientes** a la fecha de observación. Ventana alineada con NIIF 9 (etapa 1) y SARC.
- **Exclusiones**: clientes con < 6 meses de antigüedad (van a un modelo de originación), clientes ya en mora 90+, reestructurados en los últimos 6 meses.
- **Actualización continua**: recalificación **mensual** de toda la cartera + **recálculo diario** cuando ocurre un evento disparador: primer atraso, caída o desaparición de nómina, utilización de cupo > 90%, nueva consulta masiva en centrales.

### Variables (familias)
| Familia | Ejemplos | Racional de negocio |
|---|---|---|
| Comportamiento de pago | máx. días de mora 3/6/12m, # pagos mínimos, % pagado vs facturado | El mejor predictor de mora futura es el comportamiento reciente |
| Utilización | utilización cupo actual, tendencia 3m, # avances en efectivo | Clientes que "se apalancan" en el cupo anticipan estrés |
| Ingresos y liquidez | estabilidad de abono de nómina, saldo promedio cuentas, ratio gasto/ingreso | Pérdida de ingreso precede al deterioro |
| Endeudamiento externo | deuda total en sector, # consultas recientes en centrales | Sobreendeudamiento fuera del banco |
| Relación | antigüedad, # productos, canal principal | Vinculación reduce riesgo |
| Señales del modelo B | # alertas de anomalía 3m | Comportamiento atípico como señal temprana |

### Enfoque
- **Champion**: LightGBM con **restricciones monotónicas** (p. ej. a más mora, nunca menor riesgo). Mantiene interpretabilidad y evita comportamientos absurdos que un validador rechazaría.
- **Baseline/Challenger**: **scorecard logística con WoE** — estándar de la industria, fácil de validar ante la SFC. Si LightGBM no supera al scorecard en ≥ 3 puntos de Gini, se queda el scorecard (lo simple gana).
- **Validación**: **out-of-time** (entrena 2023-01 a 2024-12, valida 2025-01 a 2025-06). Nunca partición aleatoria: en riesgo, el futuro no se parece al pasado mezclado.
- **Calibración**: isotónica sobre el set OOT para que la PD sea usable en provisiones.

### Métricas
| Tipo | Métrica | Umbral de aceptación (supuesto) |
|---|---|---|
| Discriminación | Gini / KS | Gini ≥ 0,55 · KS ≥ 0,40 |
| Calibración | Brier, PD esperada vs observada por banda | Desviación ≤ 10% por banda |
| Estabilidad | PSI del score (desarrollo vs OOT) | < 0,10 |
| Negocio | Tasa de mora 90+ por banda; % de malos capturados en el 20% más riesgoso | Bandas monotónicas · captura ≥ 55% |
| Equidad | Diferencia de tasa de aprobación entre grupos (edad, género, región) a igual riesgo | Revisión por validación |

### Salida (contrato)
`cliente_id, fecha, pd_12m, score (300-950), banda (A-E), delta_vs_mes_anterior, razon_1..3, version_modelo`

---

## Modelo B — Comportamiento transaccional atípico

### Definición
- **Unidad**: transacción (y agregados por cliente en ventanas móviles).
- **Etiquetas**: fraude confirmado (contracargos, reclamos procedentes, casos de investigación). Rezago 30-60 días. Tasa ~0,1%.
- **Problema real**: (1) desbalance extremo, (2) etiquetas sesgadas (solo se etiqueta lo investigado), (3) el fraude **cambia** más rápido que el histórico.

### Enfoque híbrido
| Componente | Rol |
|---|---|
| **LightGBM supervisado** (con `scale_pos_weight` y submuestreo de negativos) | Detecta patrones de fraude **conocidos** |
| **Isolation Forest** sobre perfil de comportamiento del cliente | Detecta **novedades**: lo que se sale del patrón propio del cliente |
| **Motor de reglas existente** | Se mantiene para casos regulatorios y obvios; el modelo lo complementa, no lo reemplaza |
| **Combinador** | `score_final = w1·p_supervisado + w2·anomalia_normalizada`, con pesos ajustados por costo; reglas duras siempre prevalecen |

### Variables
- **Desviación del perfil propio**: monto / mediana del cliente 90d, z-score de hora, comercio nuevo, país/ciudad nuevo, dispositivo nuevo.
- **Velocidad**: # transacciones 1h / 24h, monto acumulado 1h, # comercios distintos 24h.
- **Contexto**: MCC del comercio, canal, tasa de fraude histórica del comercio, tarjeta presente/no presente.
- **Riesgo del cliente**: banda del modelo A.

### Métricas
| Tipo | Métrica | Por qué |
|---|---|---|
| Técnica | **PR-AUC** (no ROC-AUC) | Con 0,1% de positivos el ROC-AUC engaña |
| Operativa | **Recall @ capacidad de revisión** (p. ej. top 2.000 alertas/día) | Los analistas son el cuello de botella |
| Negocio | **Valor de fraude detectado (COP) / valor total de fraude** | No es lo mismo detectar 10 fraudes de 50 mil que uno de 20 millones |
| Experiencia | **Falsos positivos por cada 1.000 clientes legítimos** | Bloquear a un buen cliente cuesta (llamada, abandono) |
| Servicio | Latencia p95 < 100 ms | Requisito del autorizador |

### Umbral por matriz de costos
- Costo FN = monto de la transacción (pérdida).
- Costo FP = costo de revisión (~COP 15.000) + costo de fricción (~COP 25.000, supuesto).
- El umbral óptimo minimiza `Σ costo` en validación; se expone en `configs/thresholds.yaml` y se ajusta sin reentrenar.

### Salida (contrato)
`transaccion_id, score (0-1), accion_sugerida (aprobar / step-up / revisar / bloquear), razones_1..3, componente_dominante, version_modelo, latencia_ms`

---

## Explicabilidad accionable
`explainability/` calcula SHAP y lo **traduce** con un diccionario de negocio:

| SHAP técnico | Mensaje para negocio |
|---|---|
| `util_cupo_actual = 0.92 (+0.18)` | "Uso del cupo pasó de 40% a 92% en 2 meses" |
| `max_mora_3m = 15 (+0.12)` | "Tuvo un primer atraso de 15 días" |
| `ratio_monto_mediana = 14 (+0.31)` | "Transacción 14 veces mayor a su gasto habitual" |

Esto alimenta la ficha del cliente, la cola de analistas y las respuestas del agente IA.
