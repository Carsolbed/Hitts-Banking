"""Carga de configuración por capas: base.yaml + <entorno>.yaml.

El entorno se toma de la variable RISKFRAUD_ENV (dev | stg | prod). Ningún secreto vive
en estos archivos: las credenciales se resuelven desde Azure Key Vault en tiempo de ejecución.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[3] / "configs"
VALID_ENVS = {"dev", "stg", "prod"}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


@dataclass(frozen=True)
class Settings:
    """Configuración inmutable del entorno en ejecución."""

    env: str
    raw: dict[str, Any]

    def get(self, dotted_key: str, default: Any = None) -> Any:
        """Lee una clave anidada, p. ej. ``settings.get('models.risk_score.target')``."""
        node: Any = self.raw
        for part in dotted_key.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    @property
    def catalog(self) -> str:
        return self.get("catalog.name")


def load_settings(env: str | None = None, config_dir: Path = CONFIG_DIR) -> Settings:
    env = env or os.getenv("RISKFRAUD_ENV", "dev")
    if env not in VALID_ENVS:
        raise ValueError(f"Entorno inválido: {env}. Use uno de {VALID_ENVS}")
    base = yaml.safe_load((config_dir / "base.yaml").read_text())
    override = yaml.safe_load((config_dir / f"{env}.yaml").read_text())
    return Settings(env=env, raw=_deep_merge(base, override))


def load_yaml(name: str, config_dir: Path = CONFIG_DIR) -> dict[str, Any]:
    """Carga un archivo de configuración auxiliar (features, thresholds, monitoring)."""
    return yaml.safe_load((config_dir / f"{name}.yaml").read_text())
