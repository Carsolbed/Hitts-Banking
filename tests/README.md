# Estrategia de pruebas

| Nivel | Qué valida | Cuándo corre |
|---|---|---|
| `unit/` | Métricas, PSI, compuerta de promoción, configuración | Cada Pull Request (CI) |
| `data_contracts/` | Esquema, nulos, rangos y frescura de tablas Silver/Gold | Cada ejecución de pipeline |
| `model/` | Monotonía de bandas, estabilidad, equidad, sin fuga temporal (fechas de features < fecha de observación) | Cada entrenamiento |
| `integration/` | Pipeline completo sobre muestra sintética en stg; contrato de la API | Antes de desplegar a prod |
| `load/` | Latencia p95 < 100 ms a 400 tps del endpoint de fraude | Antes de cada release de B |
