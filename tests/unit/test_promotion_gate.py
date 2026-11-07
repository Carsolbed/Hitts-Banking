from riskfraud.lifecycle.promotion import PromotionGate
from riskfraud.lifecycle.registry import ALLOWED_TRANSITIONS, ModelStage


def test_candidate_better_than_champion_is_approved():
    gate = PromotionGate(primary_metric="gini")
    result = gate.evaluate(
        candidate={"gini": 0.62, "ks": 0.45, "psi_score": 0.04},
        champion={"gini": 0.58, "ks": 0.45},
    )
    assert result.approved


def test_candidate_worse_on_primary_is_rejected():
    gate = PromotionGate(primary_metric="gini")
    result = gate.evaluate(candidate={"gini": 0.55, "psi_score": 0.02}, champion={"gini": 0.58})
    assert not result.approved


def test_unstable_candidate_is_rejected():
    gate = PromotionGate(primary_metric="gini")
    result = gate.evaluate(candidate={"gini": 0.70, "psi_score": 0.18}, champion={"gini": 0.58})
    assert not result.approved


def test_cannot_skip_validation():
    assert ModelStage.CHAMPION not in ALLOWED_TRANSITIONS[ModelStage.CANDIDATO]
