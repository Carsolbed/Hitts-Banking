# ADR-0002 · Modelo A en batch (+ eventos), Modelo B en línea

**Estado**: Aceptado · **Fecha**: 2026-11

## Contexto
Ambos modelos podrían servirse en tiempo real, pero el costo y la complejidad de operar en línea son altos.

## Decisión
- **A**: scoring batch mensual de toda la cartera + recálculo diario solo para clientes con eventos disparadores. Resultado en tabla Gold servida por API de lectura.
- **B**: endpoint en línea con latencia p95 < 100 ms, integrado al flujo de autorización.

## Razones
- El riesgo crediticio cambia en semanas, no en milisegundos; las acciones (cobranza, cupo) tampoco son instantáneas.
- El fraude ocurre en segundos; detectarlo después de autorizar ya implica pérdida.
- Todo en línea costaría ~2,5x más en infraestructura sin beneficio para A.

## Consecuencias
- (+) Costo proporcional al valor.
- (−) El score de A puede tener hasta 24 h de desfase ante eventos. Aceptable para el uso.
- (−) B requiere fallback: si no responde en 100 ms, decide el motor de reglas.
