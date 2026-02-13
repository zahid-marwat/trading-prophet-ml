"""Feature engineering utilities."""
from __future__ import annotations

import numpy as np
import pandas as pd


def add_price_transforms(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["returns"] = out["close"].pct_change()
    out["log_returns"] = np.log(out["close"]).diff()
    return out


def add_lags(df: pd.DataFrame, lags: list[int] | None = None) -> pd.DataFrame:
    lags = lags or [1, 3, 7, 30]
    out = df.copy()
    for lag in lags:
        out[f"close_lag_{lag}"] = out["close"].shift(lag)
    return out


def add_rolling_stats(df: pd.DataFrame, windows: list[int] | None = None) -> pd.DataFrame:
    windows = windows or [5, 10, 20, 50]
    out = df.copy()
    for w in windows:
        out[f"roll_mean_{w}"] = out["close"].rolling(w).mean()
        out[f"roll_std_{w}"] = out["close"].rolling(w).std()
        out[f"roll_min_{w}"] = out["close"].rolling(w).min()
        out[f"roll_max_{w}"] = out["close"].rolling(w).max()
    return out


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    index = out.index
    out["hour"] = index.hour
    out["day_of_week"] = index.dayofweek
    out["month"] = index.month
    out["quarter"] = index.quarter
    return out


def add_market_regime(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    out = df.copy()
    fast_ma = out["close"].rolling(fast).mean()
    slow_ma = out["close"].rolling(slow).mean()
    out["regime"] = np.where(fast_ma > slow_ma, "bull", "bear")
    return out
