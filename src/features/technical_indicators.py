"""Technical indicator calculations."""
from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add a comprehensive set of technical indicators."""
    out = df.copy()
    try:
        import pandas_ta as ta
    except ImportError:  # pragma: no cover
        logger.warning("pandas-ta not available; returning input data")
        return out

    # Moving Averages
    out["sma_20"] = ta.sma(out["close"], length=20)
    out["ema_20"] = ta.ema(out["close"], length=20)

    # MACD
    macd = ta.macd(out["close"])
    if macd is not None:
        out["macd"] = macd.iloc[:, 0]
        out["macd_hist"] = macd.iloc[:, 1]
        out["macd_signal"] = macd.iloc[:, 2]

    # RSI
    out["rsi_14"] = ta.rsi(out["close"], length=14)

    # Bollinger Bands
    bb = ta.bbands(out["close"], length=20)
    if bb is not None:
        out["bb_lower"] = bb.iloc[:, 0]
        out["bb_mid"] = bb.iloc[:, 1]
        out["bb_upper"] = bb.iloc[:, 2]

    # Other indicators (optional, can keep or remove if not used)
    # Keeping minimal set for cleaner dataframe
    
    return out
