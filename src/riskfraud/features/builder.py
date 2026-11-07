"""Construcción de variables declaradas en `configs/features.yaml`.

Regla de oro: toda variable se calcula **point-in-time**, es decir, solo con información
disponible antes de la fecha de observación. Así se evita la fuga de información (leakage),
que infla las métricas en desarrollo y falla en producción.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession


@dataclass
class FeatureSpec:
    name: str
    family: str
    source: str | None = None
    agg: str | None = None
    window: str | None = None
    monotone: int = 0


class FeatureRegistry:
    """Lee y valida la definición declarativa de variables por modelo."""

    def __init__(self, features_config: dict) -> None:
        self.config = features_config

    def specs(self, model_name: str) -> list[FeatureSpec]:
        return [FeatureSpec(**f) for f in self.config[model_name]["features"]]

    def monotone_constraints(self, model_name: str) -> list[int]:
        """Vector de restricciones monotónicas en el orden de las variables (para LightGBM)."""
        return [s.monotone for s in self.specs(model_name)]


class FeatureBuilder:
    """Calcula variables a partir de tablas Silver y las publica en el Feature Store."""

    def __init__(self, spark: SparkSession, registry: FeatureRegistry, catalog: str) -> None:
        self.spark = spark
        self.registry = registry
        self.catalog = catalog

    def build_risk_features(self, as_of_month: str) -> DataFrame:
        """Variables cliente-mes para el modelo A."""
        raise NotImplementedError

    def build_tx_features_streaming(self, tx_stream: DataFrame) -> DataFrame:
        """Variables de velocidad y desviación de perfil con ventanas deslizantes (modelo B)."""
        raise NotImplementedError

    def publish(self, df: DataFrame, table: str, primary_keys: list[str], timestamp_key: str) -> None:
        """Escribe en Feature Store (offline) y sincroniza el online store si aplica."""
        raise NotImplementedError


class PointInTimeJoiner:
    """Une etiquetas con variables respetando la fecha de observación (as-of join)."""

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark

    def build_training_set(
        self, labels: DataFrame, feature_tables: list[str], entity_key: str, timestamp_key: str
    ) -> DataFrame:
        raise NotImplementedError
