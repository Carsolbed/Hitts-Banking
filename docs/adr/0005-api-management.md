# ADR-0005 · Exposición vía Azure API Management

**Estado**: Aceptado · **Fecha**: 2026-11

## Contexto
Los resultados serán consumidos por múltiples sistemas (agente IA, CRM, cobranza, autorizador, futuros canales). Se requiere acceso controlado.

## Decisión
Toda salida de modelos se expone por **Azure API Management** con contrato OpenAPI versionado. Ningún consumidor accede directo a tablas o endpoints de modelo.

## Razones
- Un solo punto de autenticación (OAuth2/Entra ID), autorización por *scope*, cuotas y auditoría.
- Desacopla consumidores de la implementación: se puede cambiar el modelo o el backend sin romperlos.
- Facilita incorporar nuevos consumidores ("necesidades futuras del negocio" del enunciado).

## Consecuencias
- (+) Gobierno y seguridad centralizados.
- (−) Agrega ~5-10 ms de latencia. Para el autorizador (B) se usa APIM en la misma región y política de caché desactivada.
