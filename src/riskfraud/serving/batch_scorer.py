"""Scoring batch del modelo A (mensual y diario por eventos)."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession


class BatchScorer:
    """Califica la cartera con el modelo @champion y escribe en gold.scores_riesgo.

    Cada fila guarda version_modelo y run_id → cualquier score es reproducible.
    """

    def __init__(self, spark: SparkSession, model_uri: str, output_table: str) -> None:
        self.spark = spark
        self.model_uri = model_uri
        self.output_table = output_table

    def score_full_portfolio(self, as_of_month: str) -> DataFrame:
        raise NotImplementedError

    def score_event_triggered(self, as_of_date: str) -> DataFrame:
        """Recalcula solo clientes con eventos disparadores (configs/thresholds.yaml)."""
        raise NotImplementedError

    def detect_triggered_clients(self, as_of_date: str) -> DataFrame:
        raise NotImplementedError

    def write(self, scores: DataFrame) -> None:
        """MERGE en Delta: un registro vigente por cliente + historial."""
        raise NotImplementedError
