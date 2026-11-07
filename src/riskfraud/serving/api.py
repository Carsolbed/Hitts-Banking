"""API de inferencia y consulta (FastAPI). Detrás de Azure API Management.

- Modelo B: inferencia online con presupuesto de 100 ms y fallback a reglas.
- Modelo A: lectura del score vigente desde la tabla Gold (no se recalcula en línea).
El contrato publicado está en api/openapi.yaml.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException

from riskfraud.common.contracts import FraudScoreInput, FraudScoreOutput, RiskScoreOutput

app = FastAPI(title="riskfraud API", version="1.0.0")


class ModelLoader:
    """Carga el modelo apuntado por el alias @champion y lo mantiene en memoria."""

    def __init__(self, model_uri: str) -> None:
        self.model_uri = model_uri
        self._model = None

    def get(self):
        raise NotImplementedError


class FeatureLookup:
    """Lee variables en línea (online store) para una transacción."""

    def get_online_features(self, payload: FraudScoreInput) -> dict:
        raise NotImplementedError


class RiskScoreRepository:
    """Consulta el score vigente y su historial en gold.scores_riesgo."""

    def latest(self, cliente_id: str) -> RiskScoreOutput | None:
        raise NotImplementedError

    def history(self, cliente_id: str, months: int = 12) -> list[RiskScoreOutput]:
        raise NotImplementedError


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/fraud/score", response_model=FraudScoreOutput)
def score_transaction(payload: FraudScoreInput, loader: ModelLoader = Depends()) -> FraudScoreOutput:
    """Calcula el score de la transacción. Si se excede el presupuesto de latencia,
    responde con la decisión del motor de reglas y lo registra."""
    raise NotImplementedError


@app.get("/v1/risk/clients/{cliente_id}", response_model=RiskScoreOutput)
def get_risk(cliente_id: str, repo: RiskScoreRepository = Depends()) -> RiskScoreOutput:
    result = repo.latest(cliente_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Cliente sin score vigente")
    return result
