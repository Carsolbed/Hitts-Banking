"""Herramientas (function calling) que el agente IA de negocio puede invocar.

Principios (ADR-0006):
- Solo lectura: ninguna herramienta modifica productos o clientes.
- Las acciones sugeridas salen de una tabla de políticas aprobada, no del LLM.
- Autorización heredada del usuario final: el agente solo ve lo que el usuario puede ver.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]   # JSON Schema para function calling
    handler: Callable[..., dict]


class RiskFraudApiClient:
    """Cliente HTTP hacia API Management con el token delegado (on-behalf-of) del usuario."""

    def __init__(self, base_url: str, user_token: str) -> None:
        self.base_url = base_url
        self.user_token = user_token

    def get(self, path: str, params: dict | None = None) -> dict:
        raise NotImplementedError


class PolicyTable:
    """Tabla aprobada por comité: (banda, evento) → acción recomendada."""

    def lookup(self, banda: str, eventos: list[str]) -> dict:
        raise NotImplementedError


class AgentToolkit:
    def __init__(self, api: RiskFraudApiClient, policies: PolicyTable) -> None:
        self.api = api
        self.policies = policies

    def get_risk_profile(self, cliente_id: str) -> dict:
        return self.api.get(f"/v1/risk/clients/{cliente_id}")

    def explain_change(self, cliente_id: str, meses: int = 3) -> dict:
        return self.api.get(f"/v1/risk/clients/{cliente_id}/history", {"months": meses})

    def get_fraud_alerts(self, cliente_id: str | None = None, estado: str = "pendiente") -> dict:
        return self.api.get("/v1/fraud/alerts", {"cliente_id": cliente_id, "estado": estado})

    def portfolio_summary(self, segmento: str) -> dict:
        raise NotImplementedError

    def suggest_action(self, cliente_id: str) -> dict:
        profile = self.get_risk_profile(cliente_id)
        return self.policies.lookup(profile["banda"], profile.get("eventos", []))

    def specs(self) -> list[ToolSpec]:
        """Declaración de herramientas para Azure OpenAI function calling."""
        return [
            ToolSpec(
                "get_risk_profile",
                "Score, banda, tendencia y razones de riesgo de un cliente",
                {"type": "object", "properties": {"cliente_id": {"type": "string"}}, "required": ["cliente_id"]},
                self.get_risk_profile,
            ),
            ToolSpec(
                "explain_change",
                "Explica por qué cambió el riesgo de un cliente en los últimos meses",
                {
                    "type": "object",
                    "properties": {"cliente_id": {"type": "string"}, "meses": {"type": "integer"}},
                    "required": ["cliente_id"],
                },
                self.explain_change,
            ),
            ToolSpec(
                "get_fraud_alerts",
                "Alertas de comportamiento atípico, opcionalmente por cliente",
                {"type": "object", "properties": {"cliente_id": {"type": "string"}, "estado": {"type": "string"}}},
                self.get_fraud_alerts,
            ),
            ToolSpec(
                "suggest_action",
                "Acción recomendada según la política aprobada para el cliente",
                {"type": "object", "properties": {"cliente_id": {"type": "string"}}, "required": ["cliente_id"]},
                self.suggest_action,
            ),
        ]
