"""Seguimiento de desempeño real con etiquetas tardías y proxies tempranos."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class PerformanceSnapshot:
    model: str
    version: str
    period: date
    metric: str
    value: float
    is_proxy: bool   # True si es indicador temprano (mora 30+, confirmación de analista)
    segment: str = "global"


class PerformanceTracker:
    """Une predicciones históricas con resultados observados.

    - Modelo A: target final a 12 meses; proxy a 1-3 meses (rodamiento, mora 30+).
    - Modelo B: contracargos a 30-60 días; proxy con confirmación del analista (1-2 días).
    """

    def __init__(self, model_name: str, config: dict) -> None:
        self.model_name = model_name
        self.config = config

    def compute_proxy_metrics(self, as_of: date) -> list[PerformanceSnapshot]:
        raise NotImplementedError

    def compute_final_metrics(self, as_of: date) -> list[PerformanceSnapshot]:
        raise NotImplementedError

    def compute_business_kpis(self, as_of: date) -> dict[str, float]:
        """COP de fraude evitado, mora gestionada, falsos positivos por 1.000 clientes."""
        raise NotImplementedError

    def is_degraded(self, snapshots: list[PerformanceSnapshot]) -> bool:
        raise NotImplementedError
