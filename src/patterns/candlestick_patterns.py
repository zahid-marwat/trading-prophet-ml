"""Candlestick pattern detection."""
from __future__ import annotations

import pandas as pd


def detect_candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Detect classic candlestick patterns with confidence scores."""
    out = df.copy()
    try:
        import pandas_ta as ta
    except ImportError:  # pragma: no cover
        out["pattern"] = None
        out["pattern_score"] = 0.0
        return out

    patterns = {
        "hammer": ta.cdl_hammer,
        "morning_star": ta.cdl_morningstar,
        "bullish_engulfing": ta.cdl_engulfing,
        "shooting_star": ta.cdl_shootingstar,
        "evening_star": ta.cdl_eveningstar,
        "bearish_engulfing": ta.cdl_engulfing,
        "doji": ta.cdl_doji,
        "spinning_top": ta.cdl_spinningtop,
    }

    scores = {}
    for name, func in patterns.items():
        scores[name] = func(out["open"], out["high"], out["low"], out["close"]).fillna(0)

    score_df = pd.DataFrame(scores, index=out.index)
    out["pattern"] = score_df.idxmax(axis=1)
    out["pattern_score"] = score_df.max(axis=1).abs() / 100.0
    return out
