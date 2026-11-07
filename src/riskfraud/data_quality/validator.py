"""Contratos de datos entre Bronze → Silver.

Si un contrato crítico falla, el pipeline se detiene y se alerta: es preferible un score
de ayer que un score calculado con datos rotos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from pyspark.sql import DataFrame


class Severity(str, Enum):
    WARN = "warn"          # registra y continúa
    CRITICAL = "critical"  # detiene el pipeline


@dataclass
class Expectation:
    name: str
    column: str | None
    rule: str              # p. ej. "not_null", "between:0,1", "unique", "freshness_hours:26"
    severity: Severity = Severity.CRITICAL


@dataclass
class ValidationReport:
    table: str
    passed: list[str] = field(default_factory=list)
    failed: list[tuple[str, Severity, str]] = field(default_factory=list)

    @property
    def has_critical_failures(self) -> bool:
        return any(sev == Severity.CRITICAL for _, sev, _ in self.failed)


class DataContractError(Exception):
    """Se lanza cuando un contrato crítico no se cumple."""


class DataValidator:
    """Evalúa expectativas de esquema, nulos, rangos, unicidad, volumen y frescura."""

    def __init__(self, expectations: dict[str, list[Expectation]], thresholds: dict) -> None:
        self.expectations = expectations
        self.thresholds = thresholds

    def validate(self, df: DataFrame, table: str) -> ValidationReport:
        raise NotImplementedError

    def check_volume(self, df: DataFrame, table: str) -> bool:
        """Compara contra el promedio de los últimos 7 cargues (± max_volume_change_pct)."""
        raise NotImplementedError

    def enforce(self, report: ValidationReport) -> None:
        if report.has_critical_failures:
            raise DataContractError(f"Contrato roto en {report.table}: {report.failed}")
