import numpy as np

from riskfraud.evaluation.metrics import CostMatrix, gini, value_recall_at_capacity
from riskfraud.models.risk_score import RiskScoreModel


def test_gini_perfect_model():
    y = np.array([0, 0, 1, 1])
    assert gini(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0


def test_value_recall_prioritizes_amount():
    y = np.array([1, 1, 0])
    amounts = np.array([20_000_000, 50_000, 100_000])
    score = np.array([0.9, 0.5, 0.1])
    assert value_recall_at_capacity(y, score, amounts, capacity=1) > 0.99


def test_cost_matrix_threshold_in_range():
    rng = np.random.default_rng(0)
    y = rng.binomial(1, 0.05, 2_000)
    score = np.clip(y * 0.6 + rng.uniform(0, 0.5, 2_000), 0, 1)
    amounts = rng.uniform(50_000, 2_000_000, 2_000)
    t = CostMatrix().best_threshold(y, score, amounts)
    assert 0.05 <= t <= 0.95


def test_score_scale_is_monotonic():
    pds = np.array([0.01, 0.05, 0.20])
    scores = RiskScoreModel.pd_to_score(pds)
    assert scores[0] > scores[1] > scores[2]
