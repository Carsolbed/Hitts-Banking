# Model Card · `tx_anomaly` (Modelo B)

| Campo | Valor |
|---|---|
| Nombre en registro | `riskfraud.prod.tx_anomaly` |
| Dueño de negocio | Gerencia de Prevención de Fraude |
| Dueño técnico | Gerencia Analítica – Data Science / ML Engineering |
| Tipo | Modelo compuesto (pyfunc): LightGBM supervisado + Isolation Forest + combinador |
| Etiqueta | Fraude confirmado (contracargo / reclamo procedente / investigación) |
| Tasa de positivos | ~0,1% |
| Latencia objetivo | p95 < 100 ms |
| Nivel de riesgo del modelo | Alto (impacta experiencia del cliente y pérdidas) |

## Uso previsto
Priorizar transacciones para revisión, sugerir step-up (OTP) o bloqueo preventivo según política.

## Usos NO previstos
Bloqueo definitivo de productos sin revisión humana; reemplazo del monitoreo SARLAFT.

## Métricas (a completar)
| Métrica | Validación | Umbral |
|---|---|---|
| PR-AUC | – | > línea base de reglas + 30% |
| Recall en valor @ 2.000 alertas/día | – | ≥ 60% |
| Falsos positivos / 1.000 clientes | – | ≤ 3 |
| Latencia p95 | – | < 100 ms |

## Limitaciones conocidas
- Etiquetas sesgadas hacia lo investigado; mitigado con muestra aleatoria de revisión (0,5%).
- Clientes nuevos sin perfil: el componente no supervisado es menos confiable los primeros 30 días.

## Fallback
Si el endpoint no responde en 100 ms → decide el motor de reglas.
