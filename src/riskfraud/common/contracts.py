"""Contratos de salida de los modelos. Son la interfaz estable hacia APIs, agente y tableros."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class RiskBand(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class FraudAction(str, Enum):
    APROBAR = "aprobar"
    STEP_UP_OTP = "step_up_otp"
    REVISAR = "revisar"
    BLOQUEAR_PREVENTIVO = "bloquear_preventivo"


class Reason(BaseModel):
    """Razón de negocio derivada de SHAP."""

    feature: str
    contribution: float
    message: str = Field(..., description="Texto entendible por negocio")


class RiskScoreOutput(BaseModel):
    cliente_id: str
    fecha: date
    pd_12m: float = Field(..., ge=0, le=1)
    score: int = Field(..., ge=300, le=950)
    banda: RiskBand
    delta_vs_mes_anterior: int
    razones: list[Reason] = Field(..., max_length=3)
    version_modelo: str


class FraudScoreInput(BaseModel):
    transaccion_id: str
    cliente_id: str
    monto: float
    fecha_hora: datetime
    mcc: str
    canal: str
    pais: str
    dispositivo_id: str | None = None
    tarjeta_presente: bool


class FraudScoreOutput(BaseModel):
    transaccion_id: str
    score: float = Field(..., ge=0, le=1)
    accion_sugerida: FraudAction
    razones: list[Reason] = Field(..., max_length=3)
    componente_dominante: str
    version_modelo: str
    latencia_ms: float
