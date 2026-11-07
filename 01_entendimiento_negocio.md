# 01 · Entendimiento del negocio

**Prueba técnica:** Data Scientist Senior — Hitss Colombia — Gerencia Analítica  
**Versión:** 1.0 · **Fecha:** 7 de noviembre de 2026  
**Ubicación propuesta en GitHub:** `docs/01_entendimiento_negocio.md`  
**Estado:** documento de diseño para revisión; sin implementación, datos bancarios ni resultados experimentales.

## 1. Resumen ejecutivo

Se propone una solución bancaria para anticipar el deterioro financiero de clientes, priorizar la investigación de transacciones atípicas y poner ambos resultados al alcance de analistas mediante servicios controlados y un agente de IA. Su valor depende de mejorar decisiones dentro de la capacidad operativa del banco, no de maximizar una métrica aislada.

El MVP propuesto cubre una cartera de crédito de consumo y un canal transaccional, seleccionados con el banco según disponibilidad y calidad de datos. El primer modelo actualizaría periódicamente una estimación de incumplimiento futuro; el segundo ordenaría transacciones por atipicidad y, únicamente si existen etiquetas suficientes, por probabilidad de fraude. El agente consultaría evidencias autorizadas, explicaría los resultados y sugeriría pasos de revisión. Las decisiones sensibles seguirían bajo responsabilidad humana.

La entrega de esta prueba es el planteamiento integral de la solución: componentes y clases que deberían existir, configuraciones, controles, documentación, mockups y presentación PDF/PPT en un repositorio. El enunciado solicita pensar, diseñar e implementar una solución, pero aclara expresamente que no es necesario escribir el código: se debe plantear qué componentes y clases deberían existir. Este documento desarrolla exclusivamente la parte 1; las demás partes quedan especificadas como trabajo posterior.

## 2. Fuente, autoridad y límites de la información

La fuente de requisitos es el enunciado completo aportado por el usuario en la conversación **“Diseño Solución Ciencia Datos”**, identificada como `6aef2f9e-810c-83ea-8083-57d30bdb7eab`. Se recuperó el texto completo para construir la matriz de trazabilidad. Las recomendaciones anteriores del asistente son contexto, no requisitos oficiales de Hitss.

Convenciones de este documento:

| Marca | Significado |
|---|---|
| **R** | Requisito explícito del enunciado; identificado en la matriz como R01–R35. |
| **S** | Supuesto de trabajo realista, pendiente de contrastar con el banco. |
| **D** | Decisión propuesta y justificada; revisable con evidencia. |
| **P** | Parámetro, meta o umbral propuesto; no es un dato observado ni un acuerdo del banco. |
| **ND** | No disponible o no medido. Nunca se interpreta como cero. |

No se conocen volúmenes, tasas de incumplimiento o fraude, capacidades de investigación, costos, nube específica, presupuesto, acuerdos de servicio ni datos históricos. No se afirma cumplimiento normativo: el banco deberá identificar y validar sus obligaciones aplicables con sus responsables. No se presentan probabilidades, ahorros, métricas o baselines calculados. Las cifras de diseño de este documento están marcadas como propuestas.

El contexto recuperado fija cuatro fases y doce partes, pero no enumera los doce nombres. La siguiente descomposición completa ese vacío como **propuesta**, conservando las fases y el orden acordados.

## 3. Plan de las doce partes y dependencias

Los archivos son destinos propuestos: su aparición aquí no significa que ya existan.

| Parte | Fase y contenido | Evidencia / archivo propuesto | Depende de |
|---|---|---|---|
| P01 | Diseño: entendimiento del negocio | `docs/01_entendimiento_negocio.md` | Enunciado |
| P02 | Diseño: arquitectura híbrida, seguridad y decisiones | `docs/02_arquitectura.md`, diagramas y registro de decisiones | P01 |
| P03 | Diseño: fuentes, contratos, calidad y variables temporales | `docs/03_datos.md`, diccionario y contratos | P01, P02 |
| P04 | Ciencia de datos: riesgo financiero dinámico | `docs/04_modelo_riesgo.md`, protocolo de evaluación | P01, P03 |
| P05 | Ciencia de datos: anomalías y fraude | `docs/05_modelo_anomalias_fraude.md`, protocolo de evaluación | P01, P03 |
| P06 | Ingeniería: componentes, entornos, orquestación y repetibilidad | `docs/06_ingenieria_entornos.md`, interfaces y configuraciones de referencia | P02–P05 |
| P07 | Operación: MLOps, versiones, aprobación y promoción | `docs/07_ciclo_vida.md`, estados, controles y rollback | P04–P06 |
| P08 | Operación: consumo, API y agente de IA | `docs/08_consumo_agente.md`, contratos y herramientas autorizadas | P02, P04–P07 |
| P09 | Operación: monitoreo, incidentes y mejora | `docs/09_monitoreo.md`, alertas y manuales operativos | P03–P08 |
| P10 | Entrega: caso económico, recursos, cronograma y evolución | `docs/10_plan_valor_costos.md`, estimaciones por escenarios | P01–P09 |
| P11 | Entrega: repositorio y mockups integrados | `README.md`, `docs/11_mockups_entrega.md`, índice y controles | P01–P10 |
| P12 | Sustentación: presentación y defensa de decisiones | `presentation/`, `docs/12_sustentacion.md`, PDF/PPT | P01–P11 |

Ruta crítica propuesta: confirmar etiquetas y acceso → contratos temporales → evaluación retrospectiva → controles de promoción → piloto → validación de valor. Se pueden diseñar arquitectura y mockups en paralelo, pero no certificar desempeño sin datos y etiquetas maduras.

## 4. Problema, causas hipotéticas y decisiones de negocio

### 4.1 Riesgo financiero

El banco necesita reconocer a tiempo clientes cuya capacidad o comportamiento de pago se deteriora. La hipótesis de trabajo es que consultar señales aisladas o revisiones poco frecuentes dificulta priorizar la gestión preventiva. Esta hipótesis debe contrastarse con el proceso actual; no se afirma que el banco opere así.

**Decisión que se busca mejorar:** qué clientes revisar primero, con qué evidencia y qué intervención preventiva autorizada considerar. Ejemplos: verificar cambios de ingresos, revisar obligaciones o proponer contacto de acompañamiento. El score no autoriza por sí solo negar crédito, modificar cupos o realizar cobranza.

Se operacionaliza “riesgo financiero” como **riesgo de incumplimiento crediticio** de una población concreta (D01). Es una interpretación acotada para hacer el problema medible; no representa todos los riesgos de liquidez, mercado, solvencia o situación patrimonial de un cliente.

### 4.2 Atipicidad, fraude y abuso

El banco necesita identificar operaciones que merecen investigación entre muchas transacciones legítimas. Las posibles causas incluyen cambios de dispositivo, montos o frecuencias inusuales y patrones desconocidos. Son hipótesis de señales, no pruebas de conducta ilícita.

**Decisión que se busca mejorar:** qué alertas investigar dentro de una capacidad diaria K, qué comprobaciones realizar y cuándo escalar al responsable. Una anomalía puede ser legítima; fraude requiere adjudicación. El abuso puede incumplir políticas sin ser fraude. Se conservarán categorías distintas y no se entrenará una etiqueta que mezcle esas situaciones sin un protocolo explícito.

### 4.3 Integración y valor

La consulta unificada reduciría la búsqueda manual de evidencias, pero ambos modelos mantienen objetivos, etiquetas, permisos y acciones diferentes. No se sumarán sus scores en un “riesgo total”: una probabilidad de incumplimiento y una puntuación de anomalía no comparten escala ni significado.

Cadena de valor propuesta: dato válido → señal temporalmente correcta → priorización → revisión humana → acción autorizada → resultado registrado → evaluación y mejora. Sin registrar acciones y resultados no se puede atribuir valor a la solución.

## 5. Objetivos

**Objetivo general:** diseñar una solución operable, explicable y mantenible que apoye decisiones de riesgo y fraude, integre sus resultados mediante un agente de IA y permita comprobar su valor y confiabilidad durante todo el ciclo de vida.

| ID | Objetivo específico | Resultado verificable previsto | Responsable de validación |
|---|---|---|---|
| O1 | Anticipar deterioro crediticio | Evaluación temporal frente al proceso vigente y baseline simple, con calibración y priorización a capacidad fija | Riesgo / validación independiente |
| O2 | Priorizar anomalías investigables | Ranking con carga de trabajo explícita, evaluación de utilidad y fraude cuando existan etiquetas | Fraude / operaciones |
| O3 | Hacer accionables y explicables las salidas | Cada resultado incluye fecha, versión, evidencia, límites y siguiente paso permitido | Dueños de proceso |
| O4 | Habilitar consumo seguro | Contratos de servicio, permisos por rol y separación de herramientas del agente | Arquitectura / seguridad |
| O5 | Sostener confiabilidad ante cambios | Diseño de versionamiento, monitoreo, promoción, retiro y recuperación | MLOps / validación |
| O6 | Demostrar viabilidad y valor | Costos completos, beneficio incremental medible, plan y riesgos aceptados | Patrocinador / finanzas |

Los objetivos O1 y O2 no se declaran logrados en esta parte: aquí quedan definidos sus criterios y sus necesidades de información.

## 6. Stakeholders y gobierno de decisiones

Los siguientes son **roles propuestos**, no personas ni estructuras organizativas confirmadas.

| Rol | Necesidad / responsabilidad | Decisiones y aprobación |
|---|---|---|
| Patrocinador de analítica / negocio | Prioridad, recursos y resultado económico | Alcance, presupuesto y aceptación de riesgo residual |
| Dueño de riesgo crediticio | Definición de incumplimiento, cartera y acciones | Etiqueta, horizonte, capacidad y política de uso del score |
| Dueño de fraude | Taxonomía, adjudicación y reglas actuales | Etiquetas, cola de alertas y protocolo de investigación |
| Analistas de cartera y fraude | Evidencia comprensible y carga manejable | Revisión de casos, registro de acciones y retroalimentación |
| Propietarios de datos / ingeniería | Acceso, linaje, puntualidad y contratos | Fuentes autorizadas y reglas de calidad |
| Ciencia de datos | Hipótesis, variables, comparación y evaluación | Recomienda modelos; no se autoaprueba para producción |
| Validación independiente / riesgo de modelos | Robustez y limitaciones | Aprueba o rechaza aptitud analítica según gobierno del banco |
| Plataforma / MLOps / operaciones TI | Entornos, servicio, costos y recuperación | Publicación operativa con autorización y soporte |
| Seguridad, privacidad y cumplimiento | Uso permitido, minimización y auditoría | Condiciones de acceso, retención y tratamiento |
| Arquitectura y aplicaciones consumidoras | Integración y evolución | Contratos, compatibilidad y capacidad del servicio |
| Finanzas / control de gestión | Atribución de beneficios y costos | Método económico y supuestos del caso de negocio |
| Clientes afectados | Trato justo, privacidad y mecanismos de revisión | Representados mediante políticas y canales del banco |

La promoción requiere validación analítica, aprobación del dueño de negocio y habilitación operativa/seguridad conforme al gobierno acordado. El agente y el equipo de desarrollo no sustituyen esas aprobaciones. Las discrepancias se registran y escalan al patrocinador; una fecha comercial no anula controles críticos.

## 7. Supuestos y restricciones

| ID | Supuesto de trabajo, no hecho confirmado | Validación y efecto si no se cumple |
|---|---|---|
| S01 | Existe una cartera de consumo con historial de obligaciones y pagos | Riesgo confirma población; si falta, reducir a un producto con etiqueta defendible |
| S02 | Existe un identificador de cliente seudonimizable y relacionable entre fuentes | Ingeniería valida enlaces y duplicados; excluir enlaces ambiguos |
| S03 | Se dispone o se puede reconstruir cuándo cada dato estuvo disponible | Auditar tiempos; sin reconstrucción fiable no certificar evaluación histórica |
| S04 | Es posible disponer de historia suficiente para observación y maduración | Se propone explorar 24–36 meses (P), sujeto a cobertura de eventos y cambios; no garantiza suficiencia estadística |
| S05 | Las fuentes híbridas admiten extracción autorizada sin comprometer el core | Arquitectura evalúa conectividad, ventanas y alternativas; no asumir acceso directo |
| S06 | Hay etiquetas de fraude adjudicadas, aunque incompletas y tardías | Fraude cuantifica cobertura; si no, limitar el segundo modelo a anomalías y utilidad revisada |
| S07 | Existen analistas para revisar un piloto | Operaciones fija K y tiempos; si no hay capacidad, solo modo sombra |
| S08 | El banco puede proporcionar una política o proceso vigente como comparador | Si no existe baseline reproducible, documentar baseline simple y declarar la limitación |
| S09 | Un entorno empresarial aprobado puede alojar el agente | Seguridad valida proveedor y tratamiento; si no, dejar interfaz y respuestas por plantillas |
| S10 | Se puede registrar resultado y acción de los casos investigados | Sin esto, no medir impacto causal ni desempeño completo |
| S11 | El MVP será de apoyo interno y solo lectura | Cambiar a decisiones automáticas exige ampliar validación, gobierno y alcance |
| S12 | Se adopta un producto y un canal como cobertura inicial | Negocio selecciona ambos por impacto, viabilidad y representatividad |

Restricciones confirmadas: contexto bancario híbrido, dos modelos con propósitos distintos, integración con agente, ciclo de vida completo, consumo controlado y entrega de diseño en repositorio con PDF/PPT. No se fija proveedor de nube ni tecnología en P01; su elección se justificará en P02.

## 8. Contrato temporal de riesgo crediticio

### 8.1 Población, unidad y objetivo

**Población propuesta (P):** clientes con al menos una obligación activa del producto elegido, identificables y con información suficiente al corte. Excluir de la cohorte predictiva a quienes ya satisfagan la definición de incumplimiento en el corte; se gestionarían con un proceso separado. Reportar cuántos y por qué se excluyen.

**Unidad:** cliente–fecha de corte `t`. Si existen varias obligaciones del producto, el evento de cliente ocurre si cualquiera satisface la definición. La agregación, cierres, castigos, refinanciaciones y reestructuraciones deben acordarse antes de construir etiquetas; no cambiar denominadores entre modelos.

**Etiqueta propuesta (P):** `Y_r(c,t)=1` si el cliente, sin incumplimiento al corte, alcanza al menos **90 días de mora** en alguna obligación elegible durante `(t, t+90 días]`. `Y_r=0` solo si se observa íntegramente el horizonte sin ese evento. Los 90 días de mora y el horizonte de 90 días son elecciones distintas y ambas requieren aprobación de Riesgo; no se presentan como definición regulatoria o del banco.

| Elemento | Definición propuesta y tratamiento |
|---|---|
| Ventana de observación | Últimos 180 días hasta `t` (P); comparar otras ventanas en P04 |
| Horizonte | Próximos 90 días (P); predice ocurrencia de evento en esa ventana, no pérdida monetaria |
| Cadencia de puntuación | Diaria (P), después del cierre de fuentes; investigar eventos intradía como mejora |
| Cadencia de entrenamiento | Independiente; evaluación periódica mensual (P) y entrenamiento solo por evidencia o cambios aprobados |
| Cortes para entrenamiento | Mensuales inicialmente (P), evitando que clientes muy activos dominen la muestra |
| Maduración | Corte utilizable cuando `t+90 días+L_r ≤ fecha de extracción`; `L_r` es retraso validado de conciliación |
| Censura | Si falta seguimiento, marcar desconocido/censurado; no etiquetar automáticamente como 0 |
| Nuevos clientes | Cohorte separada con historia reducida y evaluación propia; abstenerse si no hay cobertura válida |
| Salida | Probabilidad de evento en 90 días, si está calibrada; bandas derivadas de capacidad y costos, no percentiles llamados probabilidades |

Ejemplo exclusivamente temporal: para un corte al final del 31 de enero de 2026, el horizonte llega al 1 de mayo de 2026. El dato solo puede usarse para entrenar después de ese día más el retraso `L_r`. No es un caso real ni un resultado de modelo.

### 8.2 Disponibilidad, fugas y evaluación

Una variable es elegible si su evento ocurrió antes o en `t` **y** estaba disponible para el banco al corte. Se requieren `event_time`, `available_at` y versión de fuente. La mora futura, pagos posteriores, decisiones de investigación futuras y correcciones conocidas después del corte no entran como variables.

La evaluación será fuera de tiempo: entrenamiento anterior a validación y prueba final posterior, con etiquetas del entrenamiento maduras antes del inicio simulado de evaluación. No usar partición aleatoria de filas como evidencia principal. P04 definirá purga de ventanas de etiqueta solapadas, simulación de fechas de entrenamiento y validación de que un mismo cliente no introduzca resultados futuros. La aparición del mismo cliente en fechas sucesivas puede representar el uso real; se reportará además desempeño en clientes nuevos y por segmentos.

Variables candidatas, sujetas a disponibilidad y uso autorizado: mora conocida, utilización, pagos, saldo, exposición, antigüedad y variaciones históricas de flujos. Ingresos inferidos no equivalen a ingresos verificados. Las explicaciones describen asociaciones del modelo, no causas probadas del deterioro.

## 9. Contrato temporal de anomalías y fraude

**Unidad:** transacción con identificador único y fecha de decisión. **Población:** operaciones del canal seleccionado que puedan evaluarse con las fuentes disponibles. La fecha de decisión importa: variables conocidas después de una autorización no pueden justificar una detección presentada como previa a ella.

| Elemento | Definición propuesta |
|---|---|
| Atipicidad | Score de desviación respecto al comportamiento histórico y pares comparables; no es una etiqueta de fraude |
| Contexto | Ventanas anteriores a la decisión de 1 hora, 24 horas, 7 y 30 días (P); transacción actual solo con campos ya disponibles |
| MVP de consumo | Priorización posterior a la transacción; objetivo inicial de alerta en ≤15 minutos desde disponibilidad completa (P) |
| Fraude positivo | Fraude confirmado mediante protocolo y evidencia del área responsable, relacionado con la transacción |
| Fraude negativo | Caso cerrado como legítimo mediante protocolo; ausencia de reporte no basta por sí sola |
| Otras categorías | Abuso confirmado, no concluyente, pendiente, reversado técnico y disputa en curso; no fusionar sin justificación |
| Horizonte de adjudicación | Observar hasta 60 días tras la transacción (P) más retraso `L_f`; ajustar a tiempos reales de disputa y cierre |
| Maduración | `t+60 días+L_f ≤ extracción`, junto con estado de adjudicación válido; persistir incertidumbre si el caso sigue abierto |
| Corrección tardía | Versionar etiqueta y fecha de conocimiento; recalcular evaluación afectada sin modificar silenciosamente el histórico |
| Evaluación | Ventanas cronológicas, deduplicación por caso/campaña y reporte por canal, segmento y madurez |

El horizonte de adjudicación es el plazo para obtener evidencia, no un horizonte de “fraude futuro”. El modelo de anomalías puntúa la operación actual. Si no hay etiquetas confiables, no se reportarán recall de fraude, probabilidad de fraude ni pérdidas evitadas como métricas verificadas.

Las investigaciones habituales producen sesgo de selección: se conoce mejor la verdad de lo previamente alertado. Se propone una muestra aleatoria autorizada de operaciones no alertadas, con revisión proporcional al riesgo y a la capacidad, para estimar cobertura y falsos negativos. P05 documentará el diseño y la incertidumbre. La precisión sobre casos revisados no se extrapolará a toda la población sin justificación.

Se propone comparar reglas actuales, baseline de desviación robusta por cliente/segmento y detector de anomalías. Un clasificador supervisado se considerará únicamente si la calidad, cobertura y madurez de etiquetas lo permiten. Los scores de anomalía no se etiquetarán como probabilidades.

## 10. Flujo de uso y contrato de resultados

1. Obtener datos autorizados desde fuentes híbridas y validar identidad, tiempos, calidad y completitud.
2. Construir variables disponibles al corte y puntuar con versiones aprobadas.
3. Registrar resultados y priorizar dentro de capacidad; separar riesgo, anomalía y fraude confirmado.
4. Permitir a analistas y aplicaciones consultar resultados según su rol.
5. Presentar explicación, evidencia, límites y recomendaciones permitidas.
6. Registrar investigación, acción, resultado y adjudicación para seguimiento y evaluación posterior.

**Campos mínimos previstos:** identificador seudónimo; producto/canal; `as_of`; fecha de disponibilidad; ventana y horizonte; score y su significado; banda/prioridad y política que la asignó; factores explicativos; referencias de evidencia; versiones de modelo, variables, datos y política; estado de calidad; antigüedad; recomendación permitida; estado de revisión; identificador de trazabilidad.

Si faltan datos críticos o se supera la vigencia acordada, devolver estado `no_disponible` o `desactualizado`; no producir una estimación silenciosa ni interpretar ausencia de score como riesgo bajo. Distinguir cambio de score por nueva información de cambio por versión del modelo.

## 11. Agente de IA para negocio

**Usuario inicial:** analista interno autenticado. **Tareas:** consultar evolución del riesgo, explicar por qué un resultado cambió, resumir evidencias transaccionales y orientar la revisión conforme a políticas vigentes. El agente no calcula probabilidades mediante texto: recupera resultados de herramientas autorizadas.

Herramientas propuestas: consulta de score histórico, consulta de alertas, recuperación de evidencias permitidas y búsqueda en políticas aprobadas y versionadas. La autorización se aplica en cada herramienta y recurso, no solo en la interfaz. Los documentos y textos recuperados se tratan como datos no confiables frente a instrucciones del agente.

Cada respuesta debe distinguir hecho de modelo, evidencia y recomendación; incluir corte, versión, fuentes y limitaciones relevantes. Si no hay acceso, evidencia o actualidad suficiente, debe abstenerse y derivar. No presentará una atribución de variables como causalidad ni concluirá que una persona cometió fraude.

Ejemplo de formato, sin datos simulados numéricos: «El resultado corresponde al corte consultado y a la versión indicada. Los factores registrados son […] y se sustentan en […]. Esto orienta una revisión; consulte el procedimiento autorizado […]. La información faltante es […]».

**Límites del MVP:** solo lectura; sin bloqueo de cuentas, aprobación o rechazo de créditos, cambio de cupos, envío de comunicaciones ni actualización autónoma de expedientes. Minimizar datos enviados al proveedor; definir retención, auditoría y tratamiento con Seguridad y Privacidad antes de habilitarlo.

P08 diseñará pruebas de autorización entre clientes/roles, inyección de instrucciones en evidencias, respuestas sin soporte, datos obsoletos, errores de herramientas, abstención y trazabilidad de llamadas. La explicación generada se evaluará además de la exactitud de los modelos.

## 12. KPIs, baselines y umbrales de aceptación propuestos

### 12.1 Reglas de medición

**Todas las líneas base observadas están en ND.** Cada baseline se medirá sobre las mismas cohortes, ventanas temporales, etiquetas maduras, capacidad y costos que la propuesta. Se congelará la prueba final antes de comparar alternativas; no se elegirán umbrales usando esa prueba. Reportar tamaños, intervalos de incertidumbre, cobertura y resultados por segmento.

Notación: `TP`, `FP`, `FN`, `TN` provienen de etiquetas válidas; `N` es el número elegible evaluado; `K` es la capacidad de revisión acordada por periodo; `p_i` es probabilidad calibrada; `y_i` es etiqueta; `B` es el valor medido del baseline. Si un denominador es cero o la etiqueta no existe, la métrica es **no estimable**, no cero. La tabla define metas candidatas para discutir; no son compromisos de producción.

| ID / dimensión | KPI y fórmula | Baseline a medir (hoy ND) | Meta o regla propuesta (P) / razón | Ventana y dueño |
|---|---|---|---|---|
| K01 Riesgo | `Recall@K = eventos positivos entre K priorizados / positivos elegibles` | Política vigente y regresión logística simple a igual K | Mejora relativa ≥10% frente al baseline operativo si B>0; límite inferior del intervalo de diferencia >0. Si B=0, acordar mejora absoluta antes de prueba | Mensual, cohortes maduras; Riesgo |
| K02 Riesgo | `Precision@K = positivos entre K / K` | Misma cola baseline | ≥B a igual K; evita ganar cobertura aumentando carga | Mensual; Riesgo |
| K03 Riesgo | `Brier = Σ(p_i−y_i)²/N`; calibración por bandas: probabilidad media frente a frecuencia observada | Prevalencia histórica del entrenamiento y logística, calibradas sin prueba | Brier ≤ baseline y brecha absoluta de calibración por banda ≤0,03 cuando haya muestra suficiente (P); si no, ampliar intervalos/no aprobar afirmación de calibración | Fuera de tiempo; validación |
| K04 Ambos | `AP = Σ(Recall_j−Recall_(j−1))·Precision_j` sobre umbrales ordenados | Prevalencia como referencia y modelos simples | Superar baseline con incertidumbre; AP (average precision) se distingue de otras integraciones PR-AUC. ROC-AUC y KS son complementarios en P04 | Evaluación temporal; ciencia de datos |
| K05 Fraude | `Precision@K = fraudes confirmados en top K / casos top K con adjudicación válida` | Reglas vigentes con misma cobertura de adjudicación | Mejora relativa ≥10% frente a B si B>0; reportar por separado pendientes/K y no extrapolar a los no revisados | Semanal tras maduración; Fraude |
| K06 Fraude | `Recall = TP/(TP+FN)`; `recall monetario = monto de fraudes detectados / monto de fraudes confirmados` | Reglas en población con verdad verificable | ≥B sin exceder capacidad; no estimar recall poblacional con solo alertas investigadas | Mensual maduro; Fraude |
| K07 Anomalías | `Utilidad@K = alertas revisadas con hallazgo accionable / alertas revisadas con cierre` | Desviación robusta y reglas; rúbrica común de hallazgo | ≥B a igual esfuerzo; doble revisión de muestra y tasa de acuerdo reportada | Semanal; operaciones |
| K08 Carga y fricción | `FPR=FP/(FP+TN)`; `carga=Σ minutos de revisión`; `tasa alertas=alertas/transacciones` | Operación vigente por canal | Carga ≤ minutos disponibles; FPR ≤B donde se pueda estimar; si solo hay casos alertados, reportar proporción de alertas legítimas y no llamarla FPR | Diario/semanal; operaciones |
| K09 Valor | `Beneficio neto incremental = pérdida control−pérdida intervención−costos incrementales−costo de fricción`, ajustado por exposición y asignación | Proceso vigente / grupo control comparable | >0 con incertidumbre y guardas de trato al cliente; no afirmar atribución causal sin piloto controlado o diseño causal defendible | Piloto y seguimiento maduro; finanzas |
| K10 Gestión | `Tiempo medio por caso = minutos activos totales / casos cerrados`; `adopción=usuarios activos/usuarios habilitados` | Medición del flujo previo | Tiempo ≤0,8·B (P) sin empeorar calidad; adopción se observa sin meta arbitraria hasta conocer usuarios | Piloto; dueños de proceso |
| K11 Datos | `Completitud crítica=registros con todos los campos críticos válidos/registros recibidos`; `frescura=hora actual−último evento disponible conciliado` | Perfil por fuente | ≥99,5% (P) y 100% de casos servidos con campos críticos válidos o abstención; puntuación diaria antes de 08:00 America/Bogota (P), sujeto a cierre real | Por lote; ingeniería |
| K12 Servicio | `Disponibilidad=solicitudes válidas atendidas/solicitudes válidas`; latencia p95=percentil 95 de tiempos; `error=fallos/solicitudes` | Prueba de carga y flujo actual | Disponibilidad ≥99,5% mensual y p95 ≤1 s para consultar score almacenado (P); alerta posterior ≤15 min desde disponibilidad (P). No incluye respuesta completa del agente | Diario/mensual; TI |
| K13 Costos | `Costo/1.000 scores=1.000·costo asignado/N_scores`; `costo/caso=costo total/casos cerrados` | Cómputo, red híbrida, almacenamiento, licencias, LLM y personas | Dentro del presupuesto aprobado, aún ND; incluir costos fijos, reprocesos e investigación | Mensual; plataforma/finanzas |
| K14 Monitoreo | `Caída relativa=(B_desempeño−desempeño_actual)/B_desempeño`; cambios de distribución por variable | Referencia congelada de validación y periodo operativo estable | Caída >10% en dos cohortes maduras (P) activa investigación; no promoción automática. Para pérdida invertir sentido. Umbrales de distribución se calibran con variación histórica | Por lote y cohorte madura; MLOps |
| K15 Gobierno | `Trazabilidad=completos/outputs auditados`; `cobertura aprobación=versiones aprobadas/versiones servidas` | Inventario inicial | 100% de versiones servidas aprobadas y resultados auditables (P, control de salida) | Cada liberación; validación/TI |
| K16 Agente | `Fundamentación=respuestas con afirmaciones materiales sustentadas/respuestas evaluables`; `autorización=accesos indebidos exitosos/intentos de prueba` | Consulta manual y plantilla determinística | Fundamentación ≥95% (P); 0 accesos indebidos y 0 acciones sensibles en batería de aceptación; cualquier fallo crítico bloquea piloto | Antes de liberación y muestra operativa; seguridad/negocio |
| K17 Agente | `Abstención correcta=casos sin evidencia resueltos con abstención/casos sin evidencia`; `exactitud herramienta=consultas correctas/consultas evaluadas` | Plantilla y consulta directa a servicio | ≥95% en ambos (P), con rúbrica y conjunto de casos representativos; reportar errores críticos individualmente | Cada versión; responsable del agente |

Justificación de magnitudes: las mejoras del 10%, reducción del 20%, tolerancia de 3 puntos porcentuales y metas de servicio son **hipótesis iniciales de negociación**, elegidas para exigir mejora material y acotar operación, sin evidencia bancaria que las respalde todavía. Se revisarán tras medir B, capacidad, variabilidad, costos de error y tamaño de muestra. No se declarará éxito por alcanzar una cifra con una muestra insuficiente. Los controles de autorización, aprobación y trazabilidad se tratan como condiciones de salida, no promedios económicos.

### 12.2 Política de umbrales y valor económico

Para riesgo, seleccionar umbral en validación según beneficio esperado de revisar un cliente, costo y eficacia de la intervención, fricción y capacidad. `Pérdida esperada = PD × LGD × EAD` solo puede estimarse si PD está calibrada y existen LGD y EAD defendibles; la PD de este MVP no convierte por sí sola un score en estimación contable o de capital.

Para fraude/anomalías, fijar top K por periodo y prioridad, con manejo documentado de empates, deduplicación y acumulación de cola. Elegir un umbral de score con datos de validación y restricciones de capacidad, no con un porcentaje arbitrario universal. Si hay sobrecarga, reducir cobertura o escalar recursos; no ocultar alertas descartadas.

No confundir monto de transacciones alertadas con pérdidas evitadas. Medir recuperación real, contrafactual y efectos adversos. En riesgo, incluir si la gestión cambió resultados; las intervenciones históricas también pueden sesgar la etiqueta. P10 diseñará piloto, costos y sensibilidad para escenarios conservador, central y exigente sin inventar cifras observadas.

## 13. Alcance y no alcance del MVP

| Dentro del MVP propuesto | Fuera del MVP / evolución condicionada |
|---|---|
| Un producto de consumo y un canal, definidos con el banco | Cobertura de todos los productos, canales y países |
| Diseño de ingesta híbrida, calidad y variables con corte temporal | Migración completa de infraestructura o sustitución del core |
| Diseño de dos modelos y comparación con baselines | Prometer superioridad analítica sin entrenar ni evaluar |
| Riesgo actualizado diariamente y anomalías posteriores a transacción | Bloqueo/autorización síncrona de pagos o scoring de originación |
| Agente interno de consulta y explicación con herramientas de lectura | Agente autónomo que decide, ejecuta acciones o contacta clientes |
| Consumo de scores y alertas mediante contratos controlados | Exposición pública de datos o APIs sin permisos |
| Registro, aprobación, monitoreo y recuperación diseñados | Aprendizaje en línea y reentrenamiento/promoción automática sin revisión |
| Piloto futuro en sombra y luego revisión asistida | Decisiones adversas automáticas o sustitución del juicio de expertos |
| Especificaciones, configuraciones de referencia y mockups de la prueba | Modelos entrenados, despliegue real y acceso a datos bancarios en esta entrega |

El MVP real requeriría implementación y validación posteriores. La prueba entrega su diseño; una maqueta o pseudocódigo no demuestra funcionamiento productivo.

## 14. Decisiones justificadas y alternativas

| ID | Decisión propuesta | Alternativa considerada y razón de descarte inicial | Condición de revisión |
|---|---|---|---|
| D01 | Acotar riesgo financiero a incumplimiento de consumo | Índice general de “salud financiera”: difícil de etiquetar y actuar de manera consistente | Negocio exige otra definición y aporta resultado verificable |
| D02 | Separar riesgo, anomalía y fraude confirmado | Score único: mezcla escalas, horizontes y responsabilidades | Solo integrar a nivel de caso con política explícita, sin sumar scores arbitrarios |
| D03 | Recalcular scores con datos nuevos; entrenar por proceso independiente | Reentrenar en cada evento: costos y cambios sin evidencia | Demostración de necesidad y controles para aprendizaje en línea |
| D04 | Empezar con producto/canal acotados y modo sombra | Lanzamiento integral: mayor superficie de fallos y menor capacidad de atribuir valor | Piloto estable, representativo y aprobado |
| D05 | Baselines simples antes de complejidad | Deep learning de entrada: costo y explicabilidad sin mejora demostrada | Ganancia temporal y económica robusta frente a alternativas simples |
| D06 | Anomalías sin etiquetas; supervisión solo con verdad suficiente | Etiquetar todo lo no reportado como legítimo: contamina evaluación | Protocolo de negativos, cobertura y maduración verificables |
| D07 | Agente con herramientas de lectura y evidencia | Acceso SQL libre o acciones autónomas: permisos difíciles de acotar y daño potencial | Gobierno específico, necesidad de negocio y evaluación adicional |
| D08 | Arquitectura proporcional a volumen, preferencia por capacidades existentes | Adoptar streaming, clústeres y múltiples plataformas sin dimensionar | Medición de volumen, latencia, confiabilidad y costo en P02 |
| D09 | Prueba fuera de tiempo y etiquetas maduras | Partición aleatoria: puede mezclar información futura y procesos históricos | Aleatoria solo como diagnóstico secundario justificado |
| D10 | Promoción aprobada, rollback y abstención por datos inválidos | Sustitución automática por drift: drift no demuestra mejor modelo | Automatización limitada a controles aprobados, nunca asumir causalidad |
| D11 | Métricas a capacidad fija y beneficio incremental | Exactitud global o ahorro bruto: ocultan desbalance y fricción | Complementar según prevalencia y proceso, sin abandonar capacidad |
| D12 | Mantener nube abierta hasta conocer restricciones | Seleccionar proveedor por preferencia: puede contrariar infraestructura y costos | P02 concreta proveedor de referencia como supuesto si no hay respuesta |

## 15. Riesgos, mitigación y aceptación residual

Probabilidad e impacto son **valoraciones cualitativas preliminares**, no mediciones. La aceptación definitiva corresponde al rol indicado; ninguna está aprobada por el banco en esta entrega.

| ID | Riesgo / valoración preliminar | Mitigación y señal de control | Residual propuesto y dueño |
|---|---|---|---|
| RK01 | Fuga temporal o etiquetas incorrectas; impacto alto | Contratos de tiempos, reconstrucción histórica y auditoría de muestras; bloquear evaluación inválida | No aceptable para aprobación; ciencia de datos / validación |
| RK02 | Etiquetas tardías o sesgadas por investigación; probabilidad alta, impacto alto | Maduración, estados desconocidos, revisión de muestra y desempeño por cobertura | Aceptar demora de medición, no afirmar recall desconocido; Fraude |
| RK03 | Falsos positivos, fricción y sobrecarga; probabilidad alta | Top K, deduplicación, seguimiento de tiempos y calidad | Aceptar carga limitada al piloto, con pausa por saturación; operaciones |
| RK04 | Falsos negativos y pérdidas; impacto alto | Reglas existentes en paralelo, revisión y medición de brechas | Aceptar cobertura incompleta solo en sombra/asistencia; Riesgo/Fraude |
| RK05 | Cambios de población, producto o comportamiento; impacto alto | Monitorear calidad, distribución, calibración y desempeño maduro; investigar antes de reentrenar | Aceptar retraso por maduración con límites y proceso vigente; MLOps |
| RK06 | Datos híbridos tardíos, caídas o duplicados; probabilidad media | Conciliación, idempotencia, marca de frescura y recuperación | Aceptar indisponibilidad visible; nunca score silenciosamente obsoleto; TI |
| RK07 | Exposición de datos o acceso indebido; impacto alto | Minimización, autorización por recurso, secretos separados, cifrado y auditoría diseñados | No aceptar vulneración conocida en salida; seguridad |
| RK08 | Alucinación o instrucciones maliciosas en evidencia; impacto alto | Herramientas acotadas, evidencia citada, abstención y batería adversaria | Tolerar errores menores solo sin efecto decisorio y dentro de rúbrica; dueño del agente |
| RK09 | Sesgo o perjuicio desigual; impacto alto | Evaluación por segmentos permitidos, proxies, cobertura y revisión humana | No aceptar disparidad material sin investigación y decisión formal; Riesgo / cumplimiento |
| RK10 | Presión por producción anticipada; probabilidad media | Reducir alcance, sombra, usuarios limitados y criterios no negociables | Aceptar menos funcionalidades, no omitir permisos o validación crítica; patrocinador |
| RK11 | Costos, capacidad o beneficio mal estimados; probabilidad media | Sensibilidad, carga representativa y costos humanos/LLM/red incluidos | Aceptar incertidumbre presupuestada en piloto; finanzas |
| RK12 | Intervenciones alteran etiquetas y bucle de retroalimentación | Registrar acción, política y fecha; control experimental cuando sea viable | Aceptar limitación causal explícita hasta estudio válido; negocio / validación |
| RK13 | Dependencia de proveedor o integración compleja | Contratos estables, exportación de artefactos y alternativa por plantillas | Aceptar dependencia reversible documentada; arquitectura |
| RK14 | Recuperación insegura o score anterior incompatible | Validar compatibilidad de datos y versión; alternativa manual/reglas aprobadas | Rollback solo si la versión sigue siendo válida; si no, suspender; TI |

### Si dirección exige salir antes

Priorizar un canal, scores almacenados, agente por plantillas o consulta limitada y modo sombra sin acciones sobre clientes. Posponer procesamiento síncrono, nuevos productos y automatizaciones. Mantener autorización, trazabilidad, contrato temporal, validación mínima, monitoreo de calidad y procedimiento de recuperación. Si esas condiciones no están listas, presentar una demostración con datos sintéticos identificados, no llamarla producción. Registrar quién acepta el riesgo, fecha, vigencia y criterio de suspensión.

## 16. Criterios de aceptación

### 16.1 Aceptación documental de P01

| ID | Criterio verificable | Estado en esta entrega |
|---|---|---|
| A01 | Separar requisitos, supuestos, decisiones y metas de datos reales | Cubierto en secciones 2, 7, 12 y 14 |
| A02 | Definir usuarios, decisiones y responsables | Cubierto en secciones 4–6 |
| A03 | Definir unidad, población, etiqueta, observación, horizonte, maduración y censura de ambos problemas | Cubierto en secciones 8–9; requiere ratificación bancaria |
| A04 | Definir KPIs con fórmulas, comparadores y reglas de aceptación | Cubierto en sección 12; baselines observados ND |
| A05 | Delimitar MVP, agente y acciones humanas | Cubierto en secciones 10–13 |
| A06 | Justificar alternativas y explicitar riesgos residuales | Cubierto en secciones 14–15 |
| A07 | Trazar todo el enunciado y las doce partes sin afirmar ejecución | Cubierto en secciones 3 y 17 |
| A08 | Registrar preguntas, dependencias y condiciones de avance | Cubierto en secciones 3 y 18 |

La parte 1 queda redactada y lista para revisión e incorporación al repositorio. No equivale a aprobación del banco ni a cierre de las otras partes.

### 16.2 Puertas propuestas para implementación y piloto futuros

- **G1 · Definición:** Riesgo y Fraude ratifican población, etiquetas, ventanas, K y acciones; propietarios autorizan las fuentes.
- **G2 · Datos:** historia utilizable, contratos y conciliación aprobados; no hay fugas temporales conocidas; cobertura y exclusiones documentadas.
- **G3 · Analítica:** baselines medidos, prueba temporal congelada, desempeño y calibración evaluados; metas finales negociadas antes de prueba; limitaciones y segmentos revisados.
- **G4 · Operación:** versión y configuración aprobadas, consumo autenticado, trazabilidad y monitoreo; prueba de carga, falla, abstención y recuperación satisfactoria.
- **G5 · Agente:** pruebas de permisos, evidencia, vigencia y abstención; ningún fallo crítico abierto en la batería de aceptación.
- **G6 · Piloto:** usuarios y capacidad confirmados; proceso vigente disponible; plan de medición, pausa y escalamiento; riesgo residual aceptado por escrito.
- **G7 · Ampliación:** resultados maduros, valor y fricción evaluados; decisión explícita sobre expansión o retiro. Ningún KPI aislado autoriza escalar.

## 17. Matriz exhaustiva de trazabilidad del enunciado disponible

Cada fila representa una obligación o criterio del texto completo recuperado. Los subaspectos se enumeran para que puedan auditarse. **“Definido” significa definido en P01; “pendiente” significa evidencia futura, no entregada.** Requisitos añadidos por criterio profesional se distinguen del enunciado en la sección siguiente.

| ID | Requisito / criterio explícito del enunciado | Respuesta en P01 | Parte principal y apoyos | Evidencia futura verificable / estado |
|---|---|---|---|---|
| R01 | Diseñar y construir una solución con enfoque productivo | §§1, 10, 16 | P02; P06–P09, P11 | Arquitectura, interfaces y controles; pendiente |
| R02 | Ciclo completo desde obtención y preparación hasta aplicaciones/usuarios y valor | §§3–5, 10, 12 | P03; P04–P09, P10 | Flujo extremo a extremo y contratos; pendiente |
| R03 | Contexto bancario, nube y storage/BD on-premise | §§1, 7 | P02; P03, P06 | Diseño híbrido y acceso; pendiente |
| R04 | Escalar, mantenerse y evolucionar sosteniblemente con negocio/usuarios | §§5, 14–15 | P02; P06, P09, P10 | Dimensionamiento y escenarios de evolución; pendiente |
| R05 | Entrenar y evaluar modelo que actualiza riesgo financiero a lo largo del tiempo | §8 | P04; P03, P07, P09 | Especificación de entrenamiento/evaluación y rescoring; pendiente; no se exige código ejecutado en esta prueba |
| R06 | Entrenar y evaluar modelo de comportamientos transaccionales atípicos: fraude, abuso o riesgo | §§4.2, 9 | P05; P03, P09 | Taxonomía, modelos y evaluación condicionada a etiquetas; pendiente |
| R07 | Usar diferentes fuentes de datos | §§7–10 | P03; P02 | Inventario, enlaces, calidad y linaje; pendiente |
| R08 | Aportar valor y alinear modelos con agente inteligente IA para negocio | §§4–5, 11–12 | P08; P04, P05, P10 | Herramientas y casos de uso con KPIs; pendiente |
| R09 | Selección de variables, enfoque de modelamiento y evaluación coherentes y justificados | §§8–9, 12, 14 | P04 y P05; P03 | Diccionario temporal, comparadores y protocolo; pendiente |
| R10 | Explicar lógica y hacer accionables los resultados | §§4, 10–11 | P08; P04, P05, P11 | Factores, evidencia, límites, acciones y mockups; pendiente |
| R11 | Versionar modelos, gestionar estados y promover en el tiempo | §§5–6, 14, 16 | P07; P06 | Estados, aprobaciones, artefactos y registro; pendiente |
| R12 | Definir modelo de entrega operativa | §§10, 13, 16 | P07; P06, P08 | Plan de liberación, responsables y recuperación; pendiente |
| R13 | Contemplar cambios de datos u objetivos manteniendo confiabilidad | §§8–9, 14–16 | P09; P07, P10 | Casos de cambio, revisión y revalidación; pendiente |
| R14 | Consumo por sistemas/aplicaciones y necesidades futuras en ecosistema digital | §§10–11 | P08; P02 | Contratos versionados e integración; pendiente |
| R15 | Acceso controlado a resultados | §§6, 10–11, 15 | P08; P02, P06 | Autenticación, autorización y auditoría; pendiente |
| R16 | Monitoreo y control en uso: evolución de comportamiento | §§12, 15–16 | P09; P07 | Tableros, métricas y responsables; pendiente |
| R17 | Identificar degradación de desempeño | §12 K14; §15 | P09; P04, P05 | Métricas maduras, alertas y respuesta; pendiente |
| R18 | Detectar cambios relevantes en datos de entrada y anticiparlos | §§12, 15 | P09; P03 | Referencias, drift, calidad y contingencias; pendiente |
| R19 | Decidir estructura de código, orquestación y arquitectura con criterio propio | §§3, 14 | P06; P02 | Componentes, responsabilidades y orquestación; pendiente |
| R20 | Solución ordenada, repetible y buenas prácticas empresariales | §§3, 16 | P06; P07, P11 | Configuración, dependencias, entornos y controles; pendiente |
| R21 | Planteamiento PDF/PPT en repositorio | §§1, 3 | P12; P11 | Presentación final enlazada desde README; pendiente |
| R22 | Código fuente planteado como componentes y clases; no se requiere hacerlo | §§1, 3, 13 | P06; P11 | Especificaciones de interfaces, entradas, salidas y responsabilidades; pendiente |
| R23 | Archivos de configuración necesarios y controles | §§3, 16 | P06; P07, P09, P11 | Configuraciones de referencia, validaciones y políticas; pendiente |
| R24 | Documentar decisiones, claridad de razonamiento, coherencia y autonomía técnica | §§2, 14–15 | P01; P02–P12 | Registro de decisiones y defensa; definido en P01, ampliación pendiente |
| R25 | Entender problema y necesidad | §§4–6 | P01 | Objetivos, procesos y usuarios; definido |
| R26 | Solidez de diseño en funcionamiento, costo, escalabilidad y performance | §§10, 12–15 | P02; P06, P08, P10 | Escenarios de carga, costo total y compromisos; pendiente |
| R27 | Calidad del planteamiento para código | §§1, 3 | P06; P11 | Contratos, modularidad y manejo de errores; pendiente |
| R28 | Preparación y metodología de entornos | §§3, 16 | P06; P07 | Separación desarrollo/validación/producción, datos y accesos; pendiente |
| R29 | Explicar todo el ciclo de vida del modelo | §§3, 5, 14–16 | P07; P03–P09 | Desde experimento hasta retiro, monitoreo y recuperación; pendiente |
| R30 | Estimar tiempo y entregables; mejoras del ciclo que aceleren desarrollo en realidad | §§3, 18 | P10; P06, P07 | Cronograma por dependencias, recursos y reutilización; pendiente |
| R31 | Métricas clave de toda la solución y valor aportado | §12 | P01; P04, P05, P08–P10 | Fórmulas definidas; medición/estimación posterior pendiente |
| R32 | Comunicar decisiones técnicas y supuestos específicos coherentes | §§2, 7, 14 | P01; P12 | Supuestos y argumentos; definidos, ratificación pendiente |
| R33 | Mockups de salidas técnicas y vista para negocio | §§10–11 | P11; P08, P12 | Pantallas y contratos con datos sintéticos señalados; pendiente |
| R34 | Mejoras/features futuras con valor | §§13, 18 | P10; P09, P12 | Roadmap priorizado por beneficio y riesgo; pendiente |
| R35 | Sustentación: producción anticipada, prioridades, alternativas descartadas y riesgos aceptados; pragmatismo de inicio a fin | §§14–16 | P12; P01, P10 | Guion de defensa y escenarios; base definida, presentación pendiente |

Cobertura de las doce partes: P01 R24–R25/R31–R32; P02 R01/R03–R04/R26; P03 R02/R07; P04 R05/R09; P05 R06/R09; P06 R19–R20/R22–R23/R27–R28; P07 R11–R12/R29; P08 R08/R10/R14–R15; P09 R13/R16–R18; P10 R26/R30/R34; P11 R21–R23/R33; P12 R21/R24/R32/R35. Las relaciones de apoyo de la tabla completan la integración.

**Controles añadidos por diseño, no citas del enunciado:** definición de etiquetas maduras y censura; evaluación temporal; distinción anomalía/fraude; capacidad K; abstención; lectura controlada del agente; revisión de sesgos; evaluación causal del valor; piloto sombra y puertas de aceptación. Se añaden porque hacen verificables la confiabilidad, el acceso controlado y la utilidad solicitados.

## 18. Dependencias, preguntas abiertas y evolución

### 18.1 Preguntas priorizadas

| ID / prioridad | Pregunta pendiente | Responsable propuesto | Dependencia / decisión provisional |
|---|---|---|---|
| Q01 / bloqueante analítico | ¿Qué significa riesgo financiero para el banco y qué producto/población cubrir? | Riesgo | P03–P04; provisional D01 y S12 |
| Q02 / bloqueante analítico | ¿Qué define incumplimiento, cómo tratar castigos, refinanciaciones, cierres y obligaciones múltiples? | Riesgo / datos | Etiquetas §8 no aprobadas |
| Q03 / bloqueante analítico | ¿Qué etiquetas de fraude/abuso existen, cómo se adjudican y cuánto tardan? | Fraude | Supervisión y métricas §9 condicionadas |
| Q04 / bloqueante de acceso | ¿Qué fuentes, permisos, retención, conectividad y nube están autorizados? | Datos / seguridad / arquitectura | P02–P03; no extraer datos sin autorización |
| Q05 / alta | ¿Existe historial de disponibilidad y correcciones para reconstruir cortes? | Ingeniería | Validez de evaluación fuera de tiempo |
| Q06 / alta | ¿Cuál es el proceso vigente, su desempeño y costo? | Operaciones / finanzas | Baselines B y caso económico ND |
| Q07 / alta | ¿Cuántos casos puede revisar cada área y con qué tiempo de respuesta? | Riesgo / Fraude | K, umbrales y colas aún sin valor |
| Q08 / alta | ¿Se necesita alerta posterior o autorización en línea? ¿Qué latencia y volumen pico? | Negocio / TI | MVP posterior; cambiar implica rediseñar P02/P08 |
| Q09 / alta | ¿Qué intervenciones están permitidas y cómo se registran sus resultados? | Negocio / cumplimiento | Medición de valor y límites del agente |
| Q10 / alta | ¿Quién aprueba modelos, liberaciones y riesgo residual? | Patrocinador / validación | Roles §6 pendientes de ratificar |
| Q11 / alta | ¿Qué proveedor de IA, datos permitidos, retención y usos están aprobados? | Seguridad / privacidad | Agente limitado o plantillas hasta aprobación |
| Q12 / media | ¿Qué segmentos requieren evaluación y qué atributos pueden tratarse legalmente? | Riesgo / cumplimiento | Equidad y monitoreo sin asumir permisos |
| Q13 / media | ¿Presupuesto, equipo, fecha objetivo y servicios reutilizables? | Patrocinador / plataforma | P10 estimará rangos, no promesa fija |
| Q14 / media | ¿Quién consume APIs y qué contratos/versiones necesita? | Aplicaciones | P08 compatibilidad y evolución |
| Q15 / media | ¿Formato final, acceso de evaluadores y restricciones del repositorio? | Candidato / contacto de la prueba | P11–P12; evitar información sensible |

Estas preguntas no impiden entregar P01, pero sí limitan qué puede aprobarse posteriormente. Las decisiones provisionales permiten desarrollar el diseño; no sustituyen respuestas del banco.

### 18.2 Estimación y mejoras futuras

P01 no fija duración real porque faltan equipo, accesos y volumen. P10 separará tiempo de preparación de la prueba de implementación bancaria, estimará esfuerzo por entregable, esperas de acceso/etiquetas y capacidad del equipo, e incluirá escenarios. Acelerar con plantillas de contratos, reutilización de ingesta/registro existentes, ambientes reproducibles y evaluación automatizada, manteniendo revisión de decisiones críticas.

Orden propuesto de evolución, condicionado a evidencia:

1. Mejorar adjudicación y retroalimentación: aumenta confiabilidad antes de añadir modelos.
2. Ampliar producto/canal únicamente tras validar transferencia y capacidad.
3. Incorporar nuevas señales autorizadas y comparar su valor incremental y costo.
4. Reducir latencia cuando el proceso demuestre beneficio de actuar antes.
5. Evaluar redes de relaciones, selección de casos para revisión y supervisión semiautomática cuando existan datos y gobierno suficientes.
6. Considerar herramientas de escritura del agente en un proyecto separado con autorizaciones y controles específicos.

## 19. Incorporación al repositorio y cierre

Guardar este archivo como `docs/01_entendimiento_negocio.md`. Para incorporarlo desde la interfaz del repositorio: abrir la carpeta `docs` (o crearla al agregar el archivo), cargar este Markdown, revisar su vista previa y guardar un commit descriptivo, por ejemplo `docs: agregar entendimiento del negocio y trazabilidad`. Incluir después un enlace desde el README. No se ha creado ni publicado un repositorio en esta entrega.

Revisión recomendada antes de avanzar: ratificar Q01–Q04, seleccionar producto/canal y registrar cualquier cambio de etiqueta, horizonte o alcance en una nueva versión. P02 debe conservar el vínculo entre decisiones de negocio, arquitectura y evidencia; las metas seguirán identificadas como propuestas hasta su validación.

**Declaración de integridad:** este archivo contiene análisis y especificaciones. No contiene modelos implementados, mediciones reales, ahorros comprobados, datos de clientes ni afirmaciones de aprobación bancaria.
