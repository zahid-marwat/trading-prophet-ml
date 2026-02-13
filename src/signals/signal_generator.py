"""Signal generation utilities."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class Signal:
    action: str
    confidence: float
    stop_loss: float | None
    take_profit: float | None
    position_size: float | None


def generate_signals(df: pd.DataFrame, threshold: float = 0.6) -> pd.DataFrame:
    out = df.copy()
    out["signal"] = "HOLD"
    out["confidence"] = 0.0
    if "prediction" in out:
        out.loc[out["prediction"] > out["close"], "signal"] = "BUY"
        out.loc[out["prediction"] < out["close"], "signal"] = "SELL"
        out["confidence"] = (out["prediction"] - out["close"]).abs() / out["close"]
        out.loc[out["confidence"] < threshold, "signal"] = "HOLD"
    return out
