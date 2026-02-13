"""Benchmark comparison utilities."""
from __future__ import annotations

import pandas as pd


def buy_and_hold(equity: pd.Series) -> float:
    return float(equity.iloc[-1] / equity.iloc[0] - 1)
