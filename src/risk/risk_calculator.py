"""Risk calculation utilities."""
from __future__ import annotations

import numpy as np
import pandas as pd


def value_at_risk(returns: pd.Series, confidence: float = 0.95) -> float:
    return float(np.quantile(returns.dropna(), 1 - confidence))


def max_position_size(capital: float, max_pct: float) -> float:
    return capital * max_pct


def correlation_risk(returns_df: pd.DataFrame) -> pd.DataFrame:
    return returns_df.corr()
