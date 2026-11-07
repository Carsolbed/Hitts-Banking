"""Detección de drift en datos de entrada y en predicciones."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def population_stability_index(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """PSI = Σ (a - e) · ln(a / e) sobre deciles de la distribución de referencia.

    Interpretación estándar en riesgo: < 0,10 estable · 0,10-0,25 vigilar · > 0,25 cambio relevante.
    """
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e_pct = np.histogram(expected, edges)[0] / len(expected)
    a_pct = np.histogram(actual, edges)[0] / len(actual)
    e_pct = np.clip(e_pct, 1e-6, None)
    a_pct = np.clip(a_pct, 1e-6, None)
    return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))


@dataclass
class DriftResult:
    feature: str
    psi: float
    status: str  # estable | vigilar | accion
    segment: str = "global"


class DriftDetector:
    """Calcula PSI por variable, por segmento y para el score, contra la referencia de entrenamiento."""

    def __init__(self, warn: float = 0.10, action: float = 0.25, bins: int = 10) -> None:
        self.warn = warn
        self.action = action
        self.bins = bins

    def classify(self, psi: float) -> str:
        if psi >= self.action:
            return "accion"
        if psi >= self.warn:
            return "vigilar"
        return "estable"

    def check_feature(self, name: str, reference: np.ndarray, current: np.ndarray, segment: str = "global") -> DriftResult:
        psi = population_stability_index(reference, current, self.bins)
        return DriftResult(feature=name, psi=psi, status=self.classify(psi), segment=segment)

    def run(self, reference_table: str, current_table: str, features: list[str], segments: list[str]) -> list[DriftResult]:
        """Ejecuta el chequeo completo sobre tablas Delta y persiste resultados en gold.monitoreo_drift."""
        raise NotImplementedError
