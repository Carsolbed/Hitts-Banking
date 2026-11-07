"""Interfaz común de modelos.

Todos los modelos exponen el mismo ciclo: fit → evaluate → explain → log. Así el pipeline de
entrenamiento, la compuerta de promoción y el serving son genéricos y sirven para modelos futuros.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class TrainingData:
    X_train: pd.DataFrame
    y_train: pd.Series
    X_oot: pd.DataFrame          # validación out-of-time
    y_oot: pd.Series
    data_version: str            # versión Delta de la tabla de entrenamiento
    feature_version: str


@dataclass
class EvaluationResult:
    technical: dict[str, float] = field(default_factory=dict)   # Gini, KS, PR-AUC...
    business: dict[str, float] = field(default_factory=dict)    # COP detectados, captura...
    by_segment: dict[str, dict[str, float]] = field(default_factory=dict)


class BaseModel(ABC):
    """Contrato que debe cumplir todo modelo de la plataforma."""

    name: str

    def __init__(self, params: dict[str, Any]) -> None:
        self.params = params
        self._model: Any = None

    @abstractmethod
    def fit(self, data: TrainingData) -> "BaseModel":
        ...

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Devuelve la probabilidad / score."""

    @abstractmethod
    def evaluate(self, data: TrainingData) -> EvaluationResult:
        ...

    @abstractmethod
    def explain(self, X: pd.DataFrame, top_k: int = 3) -> list[list[dict]]:
        """Top-k contribuciones por registro (SHAP)."""

    def log_to_mlflow(self, data: TrainingData, result: EvaluationResult) -> str:
        """Registra parámetros, métricas, versión de datos/features, firma y artefactos.

        Devuelve el run_id que liga código + datos + features + config + modelo.
        """
        raise NotImplementedError
