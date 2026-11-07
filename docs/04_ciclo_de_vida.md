# 04 · Ciclo de vida del modelo

## Estados

```
 EXPERIMENTO ──► CANDIDATO ──► VALIDADO ──► SHADOW ──► CHAMPION ──► ARCHIVADO
     │              │             │            │           │
  MLflow run    registrado    aprobado por   califica en  alias
  (dev)         en UC (stg)   validación     paralelo     @champion
                              independiente  2-4 semanas  (prod)
```

| Estado | Dónde | Quién lo mueve | Criterio de salida |
|---|---|---|---|
| Experimento | dev | Data Scientist | Supera baseline en métrica principal |
| Candidato | stg | Pipeline CI/CD | Pasa compuerta técnica automática (`PromotionGate`) |
| Validado | stg | Validación de modelos (2ª línea) | Model card + informe de validación firmado |
| Shadow | prod (sin efecto) | Pipeline | Métricas en datos reales ≥ champion; sin incidentes |
| Champion | prod | Aprobación del dueño de negocio (PR con approval) | — |
| Archivado | UC | Automático al ser reemplazado | Se conserva para auditoría (mín. 5 años) |

En Unity Catalog se implementa con **aliases**: `@challenger`, `@shadow`, `@champion`. El serving siempre apunta a `models:/riskfraud.prod.risk_score@champion`.

## Versionado (todo ligado por `run_id`)
| Artefacto | Cómo se versiona |
|---|---|
| Código | Git (tag semántico `risk-score-v1.3.0`) |
| Datos de entrenamiento | Delta Lake time travel (versión de tabla registrada en el run) |
| Features | Versión de la definición en `configs/features.yaml` + tabla del Feature Store |
| Configuración | Archivos YAML en el commit |
| Modelo | Versión en Unity Catalog Model Registry |
| Umbrales | `configs/thresholds.yaml` versionado aparte (se ajusta sin reentrenar) |

Resultado: **cualquier score emitido se puede reproducir** — requisito de auditoría y de atención de quejas del consumidor financiero.

## Compuerta de promoción (`lifecycle/promotion.py`)
Reglas automáticas antes de que un humano mire:
1. Métrica principal ≥ champion (A: Gini; B: valor de fraude detectado @ capacidad).
2. No degrada ninguna métrica secundaria más de 2%.
3. PSI del score entre entrenamiento y OOT < 0,10.
4. Monotonía de bandas (A) y latencia p95 < 100 ms (B).
5. Pruebas de equidad dentro de tolerancia.
6. Model card completa.

## Escenarios de cambio contemplados
| Escenario | Detección | Respuesta |
|---|---|---|
| Drift de datos (p. ej. inflación sube montos) | PSI por variable > 0,25 | Investigar → reentrenar → shadow → promover |
| Cambio de patrón de fraude (nueva modalidad) | Alza de anomalías sin etiqueta + reportes de analistas | Regla temporal inmediata + reentreno acelerado de B |
| Cambio de objetivo de negocio (p. ej. apetito de riesgo) | Comité | Ajuste de umbrales (sin reentrenar) o nuevo target |
| Cambio de fuente (migración del core) | Contratos de datos fallan | Pipeline se detiene; se usa último score válido; alerta |
| Choque macro (crisis, pandemia) | Desempeño real vs esperado diverge | Overlay de expertos + recalibración |
| Modelo nuevo peor en producción | Monitoreo shadow/canary | **Rollback**: mover alias `@champion` a versión anterior (minutos) |

## Reentrenamiento
| | Modelo A | Modelo B |
|---|---|---|
| Programado | Trimestral | Mensual |
| Por evento | PSI > 0,25 o caída de Gini > 5 pts | PSI > 0,25 o caída de recall@capacidad > 10% |
| Ventana | Móvil 36 meses | Móvil 12 meses (pondera lo reciente) |
