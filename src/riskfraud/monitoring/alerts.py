"""Gestión de alertas: severidad, canal, ticket y disparo de reentrenamiento."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    source: str          # data_quality | drift | performance | service
    model: str
    severity: AlertSeverity
    message: str
    suggested_action: str


class AlertManager:
    """Envía alertas a Teams/correo, crea ticket y, si aplica, dispara el job de reentrenamiento.

    Consulta el calendario de estacionalidad (configs/monitoring.yaml) para no alertar
    por cambios esperados (quincenas, primas, Black Friday).
    """

    def __init__(self, config: dict) -> None:
        self.config = config

    def is_seasonal_period(self) -> bool:
        raise NotImplementedError

    def notify(self, alert: Alert) -> None:
        raise NotImplementedError

    def trigger_retraining(self, model: str, reason: str) -> str:
        """Lanza el job de entrenamiento vía Databricks Jobs API; devuelve run_id."""
        raise NotImplementedError
