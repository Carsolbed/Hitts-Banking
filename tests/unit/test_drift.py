import numpy as np

from riskfraud.monitoring.drift import DriftDetector, population_stability_index


def test_psi_same_distribution_is_stable():
    rng = np.random.default_rng(42)
    ref = rng.normal(0, 1, 50_000)
    cur = rng.normal(0, 1, 50_000)
    assert population_stability_index(ref, cur) < 0.01


def test_psi_detects_shift():
    rng = np.random.default_rng(42)
    ref = rng.normal(0, 1, 50_000)
    cur = rng.normal(1.0, 1, 50_000)
    assert population_stability_index(ref, cur) > 0.25


def test_classification_thresholds():
    d = DriftDetector(warn=0.10, action=0.25)
    assert d.classify(0.05) == "estable"
    assert d.classify(0.15) == "vigilar"
    assert d.classify(0.30) == "accion"
