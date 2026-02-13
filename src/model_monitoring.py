"""Model monitoring utilities."""
from __future__ import annotations

import pandas as pd


def track_accuracy(predictions: pd.Series, actuals: pd.Series) -> dict:
    errors = (predictions - actuals).abs()
    return {"mae": float(errors.mean())}


def detect_drift(metric_series: pd.Series, threshold: float = 0.1) -> bool:
    return metric_series.diff().abs().iloc[-1] > threshold
