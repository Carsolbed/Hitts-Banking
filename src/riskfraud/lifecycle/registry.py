"""Gestión de versiones y estados de modelos en MLflow + Unity Catalog.

Estados: experimento → candidato → validado → shadow → champion → archivado.
Se implementan con aliases (@challenger, @shadow, @champion); el serving siempre apunta
a @champion, así cambiar de modelo o hacer rollback no requiere redesplegar.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModelStage(str, Enum):
    EXPERIMENTO = "experimento"
    CANDIDATO = "candidato"
    VALIDADO = "validado"
    SHADOW = "shadow"
    CHAMPION = "champion"
    ARCHIVADO = "archivado"


ALLOWED_TRANSITIONS: dict[ModelStage, set[ModelStage]] = {
    ModelStage.EXPERIMENTO: {ModelStage.CANDIDATO, ModelStage.ARCHIVADO},
    ModelStage.CANDIDATO: {ModelStage.VALIDADO, ModelStage.ARCHIVADO},
    ModelStage.VALIDADO: {ModelStage.SHADOW, ModelStage.ARCHIVADO},
    ModelStage.SHADOW: {ModelStage.CHAMPION, ModelStage.ARCHIVADO},
    ModelStage.CHAMPION: {ModelStage.ARCHIVADO},
    ModelStage.ARCHIVADO: set(),
}


@dataclass
class ModelVersionInfo:
    name: str
    version: str
    run_id: str
    stage: ModelStage
    metrics: dict[str, float]
    data_version: str
    git_commit: str


class InvalidTransitionError(Exception):
    pass


class ModelRegistry:
    """Envoltorio sobre MlflowClient con reglas de transición y auditoría."""

    def __init__(self, catalog: str, schema: str = "models") -> None:
        self.catalog = catalog
        self.schema = schema

    def full_name(self, model_name: str) -> str:
        return f"{self.catalog}.{self.schema}.{model_name}"

    def register(self, model_name: str, run_id: str) -> ModelVersionInfo:
        raise NotImplementedError

    def get_by_alias(self, model_name: str, alias: str) -> ModelVersionInfo:
        raise NotImplementedError

    def transition(self, info: ModelVersionInfo, target: ModelStage, approved_by: str) -> ModelVersionInfo:
        if target not in ALLOWED_TRANSITIONS[info.stage]:
            raise InvalidTransitionError(f"{info.stage} → {target} no permitido")
        raise NotImplementedError

    def rollback(self, model_name: str, reason: str) -> ModelVersionInfo:
        """Reasigna @champion a la versión champion anterior y deja registro del motivo."""
        raise NotImplementedError
