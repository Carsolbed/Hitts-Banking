# ADR-0001 · Lakehouse en Azure Databricks con Unity Catalog

**Estado**: Aceptado · **Fecha**: 2026-11

## Contexto
El banco tiene datos on-prem (core, tarjetas) y en la nube (canales, CRM). Se necesita un lugar para integrar datos, construir features, entrenar, registrar y servir modelos con gobierno centralizado.

## Opciones
1. **Azure Databricks + Unity Catalog** (datos + ML + serving + gobierno en una plataforma).
2. Azure Synapse + Azure ML (dos plataformas integradas).
3. Microsoft Fabric + Azure ML.
4. On-prem (Spark/Hadoop propio).

## Decisión
Opción 1.

## Razones
- Una sola copia de los datos: features, entrenamiento y scoring sobre las mismas tablas Delta.
- Feature Store con point-in-time joins nativo (crítico en riesgo para evitar fuga).
- MLflow y Model Registry integrados con permisos de Unity Catalog.
- Linaje automático (datos → features → modelo), útil para auditoría.
- Escala horizontal para streaming y batch.

## Consecuencias
- (+) Menos integración, menos tiempo al MVP.
- (−) Dependencia de proveedor. **Mitigación**: código en PySpark/Python estándar y MLflow open source; portable a AWS (EMR/SageMaker) o GCP.
- (−) Costo por DBU: se controla con job clusters efímeros y spot.
- Si el banco ya tiene Azure ML como estándar, se usa Azure ML para entrenamiento/serving leyendo del Lakehouse; el diseño de capas no cambia.
