"""Modelo A: Behavioral Score dinámico (PD 90+ días a 12 meses)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from riskfraud.models.base import BaseModel, EvaluationResult, TrainingData


class ScorecardBaseline(BaseModel):
    """Scorecard logística con WoE. Baseline y challenger regulatorio.

    Si el modelo champion no supera a esta línea base en >= 3 puntos de Gini, se queda el
    scorecard: más simple de validar, explicar y mantener.
    """

    name = "risk_score_scorecard"

    def fit(self, data: TrainingData) -> "ScorecardBaseline":
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def evaluate(self, data: TrainingData) -> EvaluationResult:
        raise NotImplementedError

    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        """En el scorecard la explicación es directa: puntos por variable."""
        raise NotImplementedError


class RiskScoreModel(BaseModel):
    """LightGBM con restricciones monotónicas + calibración isotónica.

    - Las restricciones vienen de `configs/features.yaml` (FeatureRegistry.monotone_constraints).
    - La calibración se ajusta sobre OOT para que la PD sea usable en provisiones.
    """

    name = "risk_score"

    def fit(self, data: TrainingData) -> "RiskScoreModel":
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def evaluate(self, data: TrainingData) -> EvaluationResult:
        """Gini, KS, Brier, PSI dev-vs-OOT, captura en top 20%, mora por banda y por segmento."""
        raise NotImplementedError

    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        raise NotImplementedError

    @staticmethod
    def pd_to_score(pd_12m: np.ndarray, base_score: int = 600, pdo: int = 40, base_odds: float = 50) -> np.ndarray:
        """Convierte PD a escala de puntos (300-950). PDO = puntos para duplicar los odds."""
        odds = (1 - pd_12m) / np.clip(pd_12m, 1e-6, None)
        factor = pdo / np.log(2)
        offset = base_score - factor * np.log(base_odds)
        return np.clip(offset + factor * np.log(odds), 300, 950).round().astype(int)

    @staticmethod
    def assign_band(pd_12m: float, bands: dict[str, list[float]]) -> str:
        for band, (low, high) in bands.items():
            if low <= pd_12m < high:
                return band
        return "E"
