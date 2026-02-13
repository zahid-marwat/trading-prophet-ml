"""Stop-loss management utilities."""
from __future__ import annotations

import pandas as pd


def fixed_stop(price: float, pct: float) -> float:
    return price * (1 - pct)


def atr_trailing_stop(df: pd.DataFrame, atr_col: str = "ATR_14", multiplier: float = 3.0) -> pd.Series:
    if atr_col not in df:
        return pd.Series(index=df.index, dtype=float)
    return df["close"] - df[atr_col] * multiplier


def dynamic_stop(price: float, volatility: float) -> float:
    return price * (1 - volatility)
