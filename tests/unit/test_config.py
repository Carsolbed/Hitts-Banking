import pytest

from riskfraud.common.config import load_settings, load_yaml


@pytest.mark.parametrize("env", ["dev", "stg", "prod"])
def test_settings_load_for_every_env(env):
    s = load_settings(env)
    assert s.catalog == f"riskfraud_{env}"
    assert s.get("models.risk_score.target") == "mora_90_12m"


def test_dev_never_uses_real_pii():
    assert load_settings("dev").get("data.use_masked_data") is True


def test_risk_features_have_monotone_constraint():
    features = load_yaml("features")["risk_score"]["features"]
    assert all("monotone" in f for f in features)
