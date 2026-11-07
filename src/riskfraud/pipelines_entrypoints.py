"""Puntos de entrada de los jobs (invocados desde pipelines/resources/jobs.yml).

Cada función orquesta componentes; no contiene lógica de negocio propia.
"""

from __future__ import annotations

from riskfraud.common.config import load_settings
from riskfraud.common.logging import get_logger

log = get_logger(__name__)


def train(model_name: str) -> None:
    """ingesta validada → features point-in-time → fit → evaluate → log MLflow →
    registro como candidato → PromotionGate."""
    settings = load_settings()
    log.info("train_start", model=model_name, env=settings.env)
    raise NotImplementedError


def score_risk(mode: str = "full") -> None:
    """mode = 'full' (mensual) | 'events' (diario por disparadores)."""
    raise NotImplementedError


def monitor(model_name: str) -> None:
    """Calidad de datos → drift → desempeño (proxy y final) → KPIs → alertas."""
    raise NotImplementedError
