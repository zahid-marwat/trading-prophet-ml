"""Simple prediction head for numeric forecasts."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class PredictionResult:
    prediction: float
    confidence: float
    method: str


def naive_linear_forecast(df: pd.DataFrame, horizon: int = 1, window: int = 30) -> PredictionResult:
    """Predict next price using mean return over a window.

    Args:
        df: DataFrame with a 'close' column.
        horizon: Forecast horizon in steps.
        window: Rolling window for mean return.

    Returns:
        PredictionResult with prediction and confidence.
    """
    close = df["close"].dropna()
    if len(close) < window + 2:
        last = float(close.iloc[-1])
        return PredictionResult(prediction=last, confidence=0.0, method="naive_last")

    returns = close.pct_change().dropna()
    mean_ret = returns.tail(window).mean()
    std_ret = returns.tail(window).std()
    last_price = float(close.iloc[-1])

    forecast = last_price * float((1 + mean_ret) ** horizon)
    confidence = float(max(0.0, 1.0 - min(1.0, std_ret * 10)))
    return PredictionResult(prediction=forecast, confidence=confidence, method="naive_linear")
