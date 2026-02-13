"""Strategy builder utilities."""
from __future__ import annotations

import pandas as pd


def trend_following(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.Series:
    fast_ma = df["close"].rolling(fast).mean()
    slow_ma = df["close"].rolling(slow).mean()
    return pd.Series((fast_ma > slow_ma).astype(int), index=df.index)


def mean_reversion(df: pd.DataFrame, rsi_col: str = "rsi_14") -> pd.Series:
    signal = pd.Series(0, index=df.index)
    if rsi_col in df:
        signal[df[rsi_col] < 30] = 1
        signal[df[rsi_col] > 70] = -1
    return signal


def breakout(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    highs = df["high"].rolling(lookback).max()
    lows = df["low"].rolling(lookback).min()
    signal = pd.Series(0, index=df.index)
    signal[df["close"] > highs] = 1
    signal[df["close"] < lows] = -1
    return signal
