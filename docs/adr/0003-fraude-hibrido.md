# ADR-0003 · Detección de anomalías híbrida (supervisado + no supervisado + reglas)

**Estado**: Aceptado · **Fecha**: 2026-11

## Contexto
Fraude ~0,1% de transacciones, etiquetas con 30-60 días de rezago y sesgadas (solo se etiqueta lo investigado). Las modalidades cambian constantemente.

## Opciones
1. Solo supervisado (GBM).
2. Solo no supervisado (Isolation Forest / autoencoder).
3. **Híbrido** supervisado + no supervisado, coexistiendo con reglas.

## Decisión
Opción 3.

## Razones
- El supervisado tiene la mejor precisión en fraude conocido.
- El no supervisado detecta desviaciones del perfil del propio cliente → modalidades nuevas.
- Las reglas existentes encapsulan requisitos regulatorios y conocimiento experto; reemplazarlas es riesgo innecesario.
- El combinador se calibra con matriz de costos, así el umbral responde al negocio.

## Consecuencias
- (+) Cobertura de patrones conocidos y nuevos.
- (−) Dos modelos que monitorear. Se registran como un solo modelo compuesto (pyfunc) con una versión.
- Se reserva un 0,5% de transacciones aleatorias para revisión manual → reduce el sesgo de etiquetas con el tiempo.
