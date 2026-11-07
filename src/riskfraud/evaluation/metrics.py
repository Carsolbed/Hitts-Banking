"""Métricas técnicas y de negocio. Las de negocio son las que deciden la promoción."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def gini(y_true: np.ndarray, y_score: np.ndarray) -> float:
    return 2 * roc_auc_score(y_true, y_score) - 1


def ks_statistic(y_true: np.ndarray, y_score: np.ndarray) -> float:
    order = np.argsort(y_score)
    y = np.asarray(y_true)[order]
    cum_bad = np.cumsum(y) / max(y.sum(), 1)
    cum_good = np.cumsum(1 - y) / max((1 - y).sum(), 1)
    return float(np.max(np.abs(cum_bad - cum_good)))


def pr_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    return float(average_precision_score(y_true, y_score))


def capture_rate_top(y_true: np.ndarray, y_score: np.ndarray, top_pct: float = 0.2) -> float:
    """% de malos capturados en el top_pct más riesgoso (modelo A)."""
    n = max(int(len(y_score) * top_pct), 1)
    idx = np.argsort(-y_score)[:n]
    return float(np.asarray(y_true)[idx].sum() / max(np.sum(y_true), 1))


def value_recall_at_capacity(
    y_true: np.ndarray, y_score: np.ndarray, amounts: np.ndarray, capacity: int
) -> float:
    """% del VALOR del fraude detectado si los analistas revisan solo `capacity` alertas (modelo B)."""
    idx = np.argsort(-y_score)[:capacity]
    fraud_value = np.sum(amounts * y_true)
    return float(np.sum(amounts[idx] * np.asarray(y_true)[idx]) / max(fraud_value, 1))


@dataclass
class CostMatrix:
    """Costo de errores en COP. Define el umbral óptimo del modelo B."""

    fp_review: float = 15_000
    fp_friction: float = 25_000

    def total_cost(self, y_true: np.ndarray, y_pred: np.ndarray, amounts: np.ndarray) -> float:
        y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
        fn_cost = np.sum(amounts[(y_true == 1) & (y_pred == 0)])
        fp_cost = np.sum((y_true == 0) & (y_pred == 1)) * (self.fp_review + self.fp_friction)
        return float(fn_cost + fp_cost)

    def best_threshold(self, y_true: np.ndarray, y_score: np.ndarray, amounts: np.ndarray) -> float:
        grid = np.linspace(0.05, 0.95, 91)
        costs = [self.total_cost(y_true, (y_score >= t).astype(int), amounts) for t in grid]
        return float(grid[int(np.argmin(costs))])
