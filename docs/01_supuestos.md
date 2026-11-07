# 01 · Supuestos del ejercicio

El enunciado no entrega datos ni cifras. Todo lo que la solución necesita y no está dado se declara aquí. **Todos los valores son supuestos de orden de magnitud para un banco mediano colombiano** y deben validarse en la fase de descubrimiento (semanas 1-2).

## Organización y regulación
| # | Supuesto |
|---|---|
| S1 | Banco mediano regulado por la **Superintendencia Financiera de Colombia (SFC)**. Aplican SARC (riesgo de crédito, Capítulo II CBCF), SARLAFT, SARO, Circular Externa 007 de 2018 (ciberseguridad y nube) y Leyes 1266/2008 y 1581/2012 (habeas data). |
| S2 | Existe un área de **validación de modelos independiente** (segunda línea de defensa) que aprueba modelos de riesgo antes de producción. |
| S3 | Existe un **motor de reglas de fraude** en operación y un equipo de analistas de fraude (~20 personas). |
| S4 | La decisión final de crédito y de bloqueo de producto es humana o de una regla aprobada por comité. El modelo informa, no decide. |

## Datos y volumen
| # | Supuesto |
|---|---|
| S5 | ~2.000.000 de clientes activos de personas; ~3.500.000 productos (tarjetas, consumo, libranza, cuentas). |
| S6 | ~5.000.000 transacciones/día; picos de 400 tps (quincenas y diciembre). |
| S7 | Histórico disponible de **36 meses** de saldos, pagos, moras y transacciones. |
| S8 | Fraude confirmado disponible vía **contracargos y reclamos** (etiqueta con 30-60 días de rezago). Tasa ~0,1% de transacciones. |
| S9 | Información de centrales de riesgo (Datacrédito/TransUnion) disponible mensualmente con autorización del cliente. |
| S10 | Fuentes on-prem: core bancario (Oracle), tarjetas (SQL Server), switch transaccional con CDC habilitable. Fuentes cloud: canales digitales y CRM. |

## Tecnología
| # | Supuesto |
|---|---|
| S11 | El banco tiene suscripción **Azure** con Entra ID y conectividad privada a on-prem (ExpressRoute/VPN). |
| S12 | Se aprueba **Azure Databricks** con Unity Catalog como plataforma de datos y ML. Si el banco usa AWS/GCP, el diseño se traslada (ver ADR-0001). |
| S13 | Power BI es la herramienta corporativa de visualización. |
| S14 | Azure OpenAI está habilitado en una región con acuerdos de residencia de datos aprobados por seguridad. |

## Negocio (para el caso de valor)
| # | Supuesto |
|---|---|
| S15 | Cartera de consumo + tarjeta: **COP 6 billones**. Pérdida crediticia anual (castigos + provisión incremental): ~4% → COP 240.000 M. |
| S16 | Pérdida anual por fraude transaccional: **COP 25.000 M**. |
| S17 | Costo cargado de un analista de fraude: COP 80 M/año. |
| S18 | TRM de referencia: **COP 4.000 / USD** (solo para convertir costos de nube). |
