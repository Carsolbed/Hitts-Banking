# Model Card · `risk_score` (Modelo A)

| Campo | Valor |
|---|---|
| Nombre en registro | `riskfraud.prod.risk_score` |
| Dueño de negocio | Gerencia de Riesgo de Crédito |
| Dueño técnico | Gerencia Analítica – Data Science |
| Tipo | Clasificación binaria calibrada (PD) |
| Algoritmo | LightGBM monotónico (champion) · Scorecard logística WoE (challenger/baseline) |
| Target | 90+ días de mora en 12 meses |
| Población | Personas naturales con ≥ 6 meses de antigüedad, sin mora 90+ vigente |
| Ventana de desarrollo | 2023-01 a 2024-12 · OOT 2025-01 a 2025-06 |
| Frecuencia de scoring | Mensual + diario por eventos |
| Nivel de riesgo del modelo | Alto (impacta provisiones y decisiones de crédito) |

## Uso previsto
Priorizar cobranza preventiva, ajustar cupos dentro de política, apoyar estimación de provisiones, filtrar preaprobados.

## Usos NO previstos
Originación de clientes nuevos; decisiones automáticas sin revisión de política.

## Métricas (a completar en desarrollo)
| Métrica | Desarrollo | OOT | Umbral |
|---|---|---|---|
| Gini | – | – | ≥ 0,55 |
| KS | – | – | ≥ 0,40 |
| PSI score | – | – | < 0,10 |
| Captura de malos en top 20% | – | – | ≥ 55% |

## Limitaciones conocidas
- Desempeño menor en independientes sin abono de nómina (menos información de ingreso).
- Sensible a choques macro; requiere overlay experto ante crisis.

## Equidad
Sin variables protegidas como entrada. Monitoreo de impacto dispar por edad, género y región.

## Historial de versiones
| Versión | Fecha | Cambio | Aprobado por |
|---|---|---|---|
| 1.0.0 | – | Versión inicial | – |
