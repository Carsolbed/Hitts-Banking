"""Ingesta desde fuentes on-prem (batch) y streaming (CDC) hacia la capa Bronze.

Bronze es inmutable: se agrega metadata de ingesta y no se transforma el dato.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from pyspark.sql import DataFrame, SparkSession


@dataclass
class IngestionResult:
    source: str
    rows: int
    watermark: datetime | None
    target_table: str


class SourceConnector(ABC):
    """Contrato común para toda fuente. Permite agregar fuentes nuevas sin tocar el pipeline."""

    def __init__(self, spark: SparkSession, source_name: str, config: dict) -> None:
        self.spark = spark
        self.source_name = source_name
        self.config = config

    @abstractmethod
    def extract(self) -> DataFrame:
        """Lee los datos nuevos desde la fuente."""

    def add_ingestion_metadata(self, df: DataFrame) -> DataFrame:
        """Agrega _ingested_at, _source y _batch_id para auditoría."""
        raise NotImplementedError

    def write_bronze(self, df: DataFrame, table: str) -> IngestionResult:
        """Escribe en Delta (append) dentro del catálogo del entorno."""
        raise NotImplementedError


class OnPremBatchExtractor(SourceConnector):
    """Extracción incremental por columna de watermark.

    En producción la copia física la hace Azure Data Factory con Self-hosted Integration
    Runtime (dentro de la red del banco) hacia una zona de aterrizaje; esta clase la lee
    y registra el último watermark procesado.
    """

    def get_last_watermark(self) -> datetime | None:
        raise NotImplementedError

    def extract(self) -> DataFrame:
        raise NotImplementedError


class StreamConsumer(SourceConnector):
    """Consume eventos CDC de transacciones desde Event Hubs (API Kafka).

    - Particionado por cliente_id para preservar orden por cliente.
    - Checkpoint en ADLS para garantizar exactly-once en Delta.
    """

    def extract(self) -> DataFrame:
        """Devuelve un DataFrame de streaming (readStream)."""
        raise NotImplementedError

    def start(self, target_table: str, checkpoint_path: str) -> None:
        raise NotImplementedError


class ConnectorFactory:
    """Crea el conector adecuado según `configs/base.yaml -> sources.<name>.mode`."""

    @staticmethod
    def create(spark: SparkSession, source_name: str, config: dict) -> SourceConnector:
        mode = config["mode"]
        if mode.startswith("batch"):
            return OnPremBatchExtractor(spark, source_name, config)
        if mode == "streaming":
            return StreamConsumer(spark, source_name, config)
        raise ValueError(f"Modo de ingesta no soportado: {mode}")
