# 09 · Sustentación: presión, alternativas, riesgos y mejoras

## ¿Qué pasa si la dirección presiona para salir a producción antes?

**Postura**: se puede salir antes, pero cambiando el **alcance**, no la **confiabilidad**.

| Se prioriza (sale primero) | Se aplaza | No se negocia |
|---|---|---|
| **Modelo B en shadow + reglas actuales**: valor rápido, riesgo bajo porque no decide solo | Agente IA | Validación out-of-time |
| **Modelo A como scorecard logística**: más rápido de validar por la SFC | Streaming completo (se puede iniciar con micro-batch de 5 min) | Monitoreo de datos y drift básico |
| Lista priorizada de clientes para cobranza (salida batch en Excel/Power BI) | Feature Store online avanzado | Rollback probado |
| | Recálculo diario por eventos de A | Trazabilidad (`run_id`) |

**Plan acelerado (6 semanas)**: S1-2 datos + línea base · S3-4 scorecard A + B supervisado · S5 shadow · S6 go-live controlado.

**Mensaje a la dirección**: "En 6 semanas tenemos valor medible y en 12 la solución completa. Saltarnos la validación ahorra 2 semanas pero arriesga una observación de la SFC o un modelo que bloquee clientes buenos en diciembre."

## Alternativas consideradas y descartadas

| Alternativa | Por qué se descartó |
|---|---|
| Deep learning (LSTM/Transformers) para A | Ganancia marginal sobre GBM en datos tabulares; difícil de explicar y validar ante la SFC |
| Solo modelo supervisado para fraude | No detecta modalidades nuevas; depende de etiquetas sesgadas |
| Solo no supervisado para fraude | Demasiadas alertas sin priorización; los analistas no dan abasto |
| Todo en tiempo real | Costo ~2,5x sin beneficio para el riesgo crediticio |
| Azure ML en lugar de Databricks | Válido, pero duplica plataforma si los datos ya viven en el Lakehouse (ver ADR-0001) |
| Modelos de grafos para anillos de fraude en el MVP | Alto valor pero alta complejidad; queda como mejora futura |
| Agente que ejecuta acciones | Riesgo regulatorio y reputacional; se limita a solo lectura |
| Reemplazar el motor de reglas | Riesgo operativo alto; las reglas tienen conocimiento regulatorio acumulado |

## Riesgos aceptados explícitamente

| Riesgo | Por qué se acepta | Mitigación |
|---|---|---|
| Etiquetas de fraude sesgadas (solo se etiqueta lo investigado) | No hay alternativa realista | Componente no supervisado + muestreo aleatorio de transacciones para revisión |
| Etiqueta de A tarda 12 meses | Es la naturaleza del riesgo de crédito | Proxies tempranos (mora 30+, rodamiento) |
| Dependencia de Databricks/Azure | Reduce tiempo y costo de integración | Código en Python/Spark estándar y MLflow open source → portable |
| MVP con menos variables de las ideales | Velocidad > perfección | Arquitectura de features extensible |
| Latencia de B depende del online store | Tradeoff costo/latencia | Fallback a reglas si el endpoint no responde en 100 ms |

## Mejoras y features futuros con valor de negocio
1. **Detección de anillos de fraude con grafos** (cuentas mula, dispositivos compartidos).
2. **Next Best Action en cobranza**: qué canal, qué oferta de reestructuración y cuándo, por cliente.
3. **Pronóstico de provisiones** NIIF 9 por escenarios macro usando las PD del modelo A.
4. **Cupos dinámicos**: aumentos/reducciones automáticas dentro de política para clientes A-B.
5. **Agente en el CRM y en WhatsApp interno** para la fuerza comercial.
6. **Modelo de originación** reutilizando el Feature Store.
7. **Detección de abuso de promociones** y de lavado (apoyo a SARLAFT).
