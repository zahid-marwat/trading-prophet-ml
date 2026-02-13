"""Candlestick pattern detection."""
from __future__ import annotations

import pandas as pd


def detect_candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Detect classic candlestick patterns with confidence scores."""
    out = df.copy()
    try:
        import talib
    except ImportError:  # pragma: no cover
        out["pattern"] = None
        out["pattern_score"] = 0.0
        return out

    patterns = {
        "hammer": talib.CDLHAMMER,
        "morning_star": talib.CDLMORNINGSTAR,
        "engulfing": talib.CDLENGULFING,
        "shooting_star": talib.CDLSHOOTINGSTAR,
        "evening_star": talib.CDLEVENINGSTAR,
        "doji": talib.CDLDOJI,
        "spinning_top": talib.CDLSPINNINGTOP,
    }

    scores = {}
    for name, func in patterns.items():
        scores[name] = func(out["open"], out["high"], out["low"], out["close"])

    score_df = pd.DataFrame(scores, index=out.index)
    out["pattern"] = score_df.idxmax(axis=1)
    out["pattern_score"] = score_df.max(axis=1).abs() / 100.0
    return out
