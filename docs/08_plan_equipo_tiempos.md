# 08 · Plan, tiempos y entregables

## Plan del MVP (12 semanas)

| Semanas | Fase | Entregables |
|---|---|---|
| 1-2 | **Descubrimiento y datos** | Supuestos validados, accesos, inventario de fuentes, contratos de datos, línea base (reglas actuales y scorecard vigente) |
| 2-3 | **Plataforma** | Workspaces dev/stg/prod con Terraform, CI/CD, ingesta Bronze/Silver, Feature Store inicial |
| 3-6 | **Modelo A** | Features, scorecard + LightGBM, validación OOT, model card, explicaciones |
| 4-8 | **Modelo B** (paralelo) | Streaming, features de velocidad, modelo híbrido, umbral por costos, endpoint |
| 7-10 | **MLOps y consumo** | Registro y compuertas, APIs en APIM, monitoreo, tablero Power BI |
| 9-11 | **Agente IA** | Herramientas, guardrails, piloto con 10-20 usuarios |
| 11-12 | **Shadow y go/no-go** | Shadow de A y B en producción, informe de validación, decisión en comité |

**Post-MVP (semanas 13-16):** promoción a champion, canary del modelo B (10% → 50% → 100% del tráfico), capacitación de usuarios.

## Ruta crítica y riesgos de cronograma
- **Acceso a datos on-prem** suele ser el mayor retraso en bancos (permisos, seguridad, firewall). Se arranca el día 1.
- **Validación independiente** tiene su propia cola: se involucra desde la semana 3, no al final.

## Aceleradores (cómo hacerlo más rápido en la realidad)
| Acelerador | Ahorro estimado |
|---|---|
| **Plantilla de repositorio MLOps** (este repo) reutilizable para cualquier modelo | 2-3 semanas por modelo nuevo |
| **Datos sintéticos** con la misma estructura para desarrollar mientras llegan los permisos | 1-2 semanas |
| **Feature Store compartido** entre A y B (y modelos futuros) | 30% del esfuerzo de features |
| **Empezar con línea base** (reglas actuales, scorecard) para tener comparativo desde el día 1 | Evita retrabajo |
| **Validador involucrado temprano** con model card viva | 2-4 semanas de validación |
| **Databricks Asset Bundles** para desplegar jobs como código | Despliegues en minutos |
| **AutoML como referencia** rápida en semana 3 (no como modelo final) | Acota el techo de desempeño |
