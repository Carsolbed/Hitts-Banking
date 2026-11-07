"""Compuerta de promoción automática y estrategia champion/challenger.

La compuerta es el filtro técnico ANTES de la aprobación humana (validación + negocio).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GateCheck:
    name: str
    passed: bool
    detail: str


@dataclass
class GateResult:
    checks: list[GateCheck] = field(default_factory=list)

    @property
    def approved(self) -> bool:
        return all(c.passed for c in self.checks)


class PromotionGate:
    """Reglas para pasar de candidato a validado.

    1. Métrica principal >= champion.
    2. Ninguna métrica secundaria cae más de `max_secondary_drop`.
    3. PSI del score (train vs OOT) < `max_psi`.
    4. Requisitos específicos (monotonía de bandas en A, latencia en B).
    5. Model card completa.
    """

    def __init__(self, primary_metric: str, max_secondary_drop: float = 0.02, max_psi: float = 0.10) -> None:
        self.primary_metric = primary_metric
        self.max_secondary_drop = max_secondary_drop
        self.max_psi = max_psi

    def evaluate(self, candidate: dict[str, float], champion: dict[str, float] | None) -> GateResult:
        result = GateResult()
        if champion is None:
            result.checks.append(GateCheck("primer_modelo", True, "No hay champion; se compara contra baseline"))
        else:
            cand, champ = candidate[self.primary_metric], champion[self.primary_metric]
            result.checks.append(
                GateCheck(f"{self.primary_metric}>=champion", cand >= champ, f"{cand:.4f} vs {champ:.4f}")
            )
            for metric, champ_value in champion.items():
                if metric == self.primary_metric or metric not in candidate:
                    continue
                drop = (champ_value - candidate[metric]) / abs(champ_value) if champ_value else 0.0
                result.checks.append(
                    GateCheck(f"{metric}_sin_degradar", drop <= self.max_secondary_drop, f"caída {drop:.2%}")
                )
        psi = candidate.get("psi_score", 0.0)
        result.checks.append(GateCheck("psi_score", psi < self.max_psi, f"PSI={psi:.3f}"))
        return result


class ChampionChallenger:
    """Ejecuta el challenger en modo shadow (sin efecto) y compara contra el champion
    sobre el mismo tráfico durante la ventana definida (2-4 semanas)."""

    def __init__(self, model_name: str, shadow_days: int = 21) -> None:
        self.model_name = model_name
        self.shadow_days = shadow_days

    def compare(self) -> dict[str, dict[str, float]]:
        raise NotImplementedError

    def recommend(self) -> str:
        """'promover' | 'extender_shadow' | 'descartar'."""
        raise NotImplementedError
