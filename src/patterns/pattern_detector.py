"""Pattern detector orchestration."""
from __future__ import annotations

import pandas as pd

from .candlestick_patterns import detect_candlestick_patterns
from .chart_patterns import detect_chart_patterns, detect_support_resistance, detect_trend_lines


def detect_patterns(df: pd.DataFrame) -> pd.DataFrame:
    out = detect_candlestick_patterns(df)
    out = detect_support_resistance(out)
    out = detect_trend_lines(out)
    out = detect_chart_patterns(out)
    return out


def pattern_signals(df: pd.DataFrame, threshold: float = 0.6) -> pd.DataFrame:
    out = df.copy()
    out["pattern_signal"] = "HOLD"
    out.loc[out["pattern_score"] >= threshold, "pattern_signal"] = "BUY"
    return out
