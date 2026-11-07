"""Modelo B: detección híbrida de comportamiento transaccional atípico.

Se registra como UN modelo compuesto (mlflow.pyfunc) para versionar y servir en conjunto.
"""

from __future__ import annotations

import pandas as pd

from riskfraud.models.base import BaseModel, EvaluationResult, TrainingData


class SupervisedFraudModel(BaseModel):
    """LightGBM sobre fraude confirmado. Maneja desbalance con submuestreo de negativos
    y corrección de probabilidad posterior."""

    name = "tx_supervised"

    def fit(self, data: TrainingData) -> "SupervisedFraudModel":
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def evaluate(self, data: TrainingData) -> EvaluationResult:
        raise NotImplementedError

    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        raise NotImplementedError


class BehaviorAnomalyModel(BaseModel):
    """Isolation Forest sobre variables de desviación del perfil propio del cliente.
    Detecta modalidades nuevas que el supervisado no ha visto."""

    name = "tx_unsupervised"

    def fit(self, data: TrainingData) -> "BehaviorAnomalyModel":
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Score de anomalía normalizado a [0, 1]."""
        raise NotImplementedError

    def evaluate(self, data: TrainingData) -> EvaluationResult:
        raise NotImplementedError

    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        raise NotImplementedError


class HybridAnomalyModel(BaseModel):
    """Combina supervisado + no supervisado y traduce el score a una acción sugerida.

    score_final = w_sup * p_supervisado + w_unsup * anomalia
    Las reglas duras del motor existente siempre prevalecen (se aplican fuera del modelo).
    """

    name = "tx_anomaly"

    def __init__(self, params: dict, thresholds: dict) -> None:
        super().__init__(params)
        self.thresholds = thresholds
        self.supervised = SupervisedFraudModel(params.get("supervised", {}))
        self.unsupervised = BehaviorAnomalyModel(params.get("unsupervised", {}))

    def fit(self, data: TrainingData) -> "HybridAnomalyModel":
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def evaluate(self, data: TrainingData) -> EvaluationResult:
        """PR-AUC, recall en valor @ capacidad, FP por 1.000 clientes, latencia."""
        raise NotImplementedError

    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        raise NotImplementedError

    def to_action(self, score: float) -> str:
        for action, (low, high) in self.thresholds["actions"].items():
            if low <= score < high or (high == 1.0 and score == 1.0):
                return action
        return "revisar"

    def optimize_weights_and_threshold(self, data: TrainingData) -> dict:
        """Busca pesos y umbrales que minimizan el costo total según la matriz de costos."""
        raise NotImplementedError
