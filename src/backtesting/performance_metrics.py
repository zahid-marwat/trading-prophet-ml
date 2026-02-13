"""Performance metric calculations."""
from __future__ import annotations

import numpy as np
import pandas as pd


def total_return(equity: pd.Series) -> float:
    return float(equity.iloc[-1] / equity.iloc[0] - 1)


def annualized_return(equity: pd.Series, periods_per_year: int = 252) -> float:
    returns = equity.pct_change().dropna()
    return float((1 + returns.mean()) ** periods_per_year - 1)


def sharpe_ratio(equity: pd.Series, periods_per_year: int = 252) -> float:
    returns = equity.pct_change().dropna()
    return float(np.sqrt(periods_per_year) * returns.mean() / returns.std())


def max_drawdown(equity: pd.Series) -> float:
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1
    return float(drawdown.min())
