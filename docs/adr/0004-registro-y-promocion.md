# ADR-0004 · Registro en MLflow/Unity Catalog con aliases y compuertas de promoción

**Estado**: Aceptado · **Fecha**: 2026-11

## Decisión
- Todo modelo se registra en Unity Catalog (`riskfraud.<entorno>.<modelo>`).
- Estados representados por **aliases**: `@challenger`, `@shadow`, `@champion`.
- Promoción solo por pipeline de CD tras pasar `PromotionGate` + aprobación humana (validación de modelos y dueño de negocio) en un Pull Request.
- Rollback = reasignar `@champion` a la versión anterior.

## Razones
- Los consumidores apuntan a un alias estable; cambiar de modelo no requiere redesplegar el serving.
- Rollback en minutos.
- Trazabilidad completa para auditoría (quién aprobó, con qué métricas, sobre qué datos).

## Consecuencias
- Requiere disciplina: nadie promueve manualmente desde la UI en prod (permisos restringidos al service principal de CD).
