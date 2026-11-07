# 10 · Seguridad, gobierno y cumplimiento

## Seguridad
- **Red**: Databricks con VNet injection y Private Link; sin endpoints públicos. Conectividad on-prem por ExpressRoute.
- **Identidad**: Entra ID para personas y *managed identities* / service principals para pipelines. Sin secretos en código: **Azure Key Vault**.
- **Cifrado**: en reposo con llaves administradas por el banco (CMK) y en tránsito TLS 1.2+.
- **Acceso a datos**: Unity Catalog con permisos por rol, **máscaras de columna** (documento, nombre, teléfono) y filtros por fila.
- **Entornos**: dev trabaja con datos enmascarados o sintéticos; solo prod ve datos personales reales.

## Gobierno de modelos
- **Inventario de modelos** en Unity Catalog con dueño, uso, nivel de riesgo y fecha de próxima revisión.
- **Model cards** obligatorias ([`model_cards/`](model_cards/)).
- **Validación independiente** antes de producción y revisión anual.
- **Comité de modelos** mensual con el tablero de monitoreo.
- **Linaje** de datos y modelos automático en Unity Catalog.

## Cumplimiento (Colombia)
| Norma | Cómo se atiende |
|---|---|
| SARC (CBCF Cap. II) | Modelo A documentado, validado, calibrado y monitoreado; resultados reproducibles |
| SARLAFT | Las alertas de B pueden alimentar el monitoreo transaccional; no lo reemplazan |
| CE 007 de 2018 (nube y ciberseguridad) | Evaluación de proveedor de nube, cifrado, residencia de datos, registro de incidentes |
| Ley 1266 / 1581 (habeas data) | Uso de datos con autorización, minimización, enmascaramiento, derecho a explicación |
| Protección al consumidor financiero | Toda decisión adversa tiene razones explicables y reproducibles |

## Equidad
- No se usan variables protegidas (género, etnia) como entrada.
- Se mide impacto dispar por edad, género y región **después** del modelo; cualquier diferencia relevante a igual nivel de riesgo se escala a validación.
