"""Paper trading simulator placeholder."""
from __future__ import annotations

import pandas as pd


def simulate_trading(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["portfolio_value"] = 1.0
    return out
