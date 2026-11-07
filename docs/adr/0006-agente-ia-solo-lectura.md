# ADR-0006 · Agente IA de solo lectura con acciones desde tabla de políticas

**Estado**: Aceptado · **Fecha**: 2026-11

## Contexto
La solución final es un agente IA para el negocio. Un LLM puede alucinar o ser manipulado (prompt injection).

## Decisión
- El agente **consulta y explica**; no ejecuta acciones sobre productos ni clientes.
- Las "acciones sugeridas" se toman de una **tabla de políticas aprobada** (banda + evento → acción), no se generan libremente.
- Autorización heredada del usuario final; registro completo de conversaciones.

## Razones
- Decisiones de crédito y bloqueo tienen impacto regulatorio y reputacional.
- Mantiene al humano en el bucle y la responsabilidad clara.
- Permite salir a producción más rápido (menor riesgo → menor fricción con seguridad y cumplimiento).

## Consecuencias
- (−) Menos automatización inicial.
- (+) Fase 2 podrá habilitar acciones de bajo riesgo (p. ej. crear tarea de cobranza) con doble confirmación.
