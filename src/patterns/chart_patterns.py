"""Chart pattern detection utilities (placeholders)."""
from __future__ import annotations

import pandas as pd


def detect_support_resistance(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["support"] = out["low"].rolling(20).min()
    out["resistance"] = out["high"].rolling(20).max()
    return out


def detect_trend_lines(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["trend"] = out["close"].rolling(50).mean()
    return out


def detect_chart_patterns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["chart_pattern"] = None
    out["pattern_confidence"] = 0.0
    return out
