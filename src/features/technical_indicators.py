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

    out = out.join(ta.sma(out["close"], length=20).rename("sma_20"))
    out = out.join(ta.ema(out["close"], length=20).rename("ema_20"))
    macd = ta.macd(out["close"])
    if macd is not None:
        out = out.join(macd)
    adx = ta.adx(out["high"], out["low"], out["close"])
    if adx is not None:
        out = out.join(adx)
    out = out.join(ta.rsi(out["close"], length=14).rename("rsi_14"))
    out = out.join(ta.stoch(out["high"], out["low"], out["close"])).rename(columns=lambda c: c)
    out = out.join(ta.cci(out["high"], out["low"], out["close"])).rename(columns=lambda c: c)
    out = out.join(ta.willr(out["high"], out["low"], out["close"])).rename(columns=lambda c: c)
    bb = ta.bbands(out["close"])
    if bb is not None:
        out = out.join(bb)
    out = out.join(ta.atr(out["high"], out["low"], out["close"])).rename(columns=lambda c: c)
    out = out.join(ta.kc(out["high"], out["low"], out["close"])).rename(columns=lambda c: c)
    out = out.join(ta.obv(out["close"], out["volume"])).rename(columns=lambda c: c)
    out = out.join(ta.mfi(out["high"], out["low"], out["close"], out["volume"])).rename(columns=lambda c: c)
    out = out.join(ta.vwap(out["high"], out["low"], out["close"], out["volume"])).rename(columns=lambda c: c)
    return out
