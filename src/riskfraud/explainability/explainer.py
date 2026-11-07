"""Explicabilidad accionable: SHAP → razones en lenguaje de negocio.

"El valor no está solo en predecir, sino en explicar la lógica." Esta capa alimenta la ficha
del cliente, la cola de analistas y las respuestas del agente IA.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from riskfraud.common.contracts import Reason


class ShapExplainer:
    """Calcula contribuciones SHAP (TreeExplainer) para modelos de árboles."""

    def __init__(self, model: Any, background: pd.DataFrame | None = None) -> None:
        self.model = model
        self.background = background

    def top_contributions(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        """Devuelve, por registro, las top_k variables que más AUMENTAN el riesgo."""
        raise NotImplementedError


class ReasonCodeTranslator:
    """Traduce contribuciones técnicas a mensajes de negocio con plantillas versionadas.

    Ejemplo de plantilla:
        util_cupo_actual: "Uso del cupo en {value:.0%} (antes {previous:.0%})"
    """

    def __init__(self, templates: dict[str, str]) -> None:
        self.templates = templates

    def translate(self, contributions: list[dict], context: dict | None = None) -> list[Reason]:
        reasons = []
        for c in contributions:
            template = self.templates.get(c["feature"], "{feature} influyó en el resultado")
            message = template.format(**{**c, **(context or {})})
            reasons.append(Reason(feature=c["feature"], contribution=c["contribution"], message=message))
        return reasons
