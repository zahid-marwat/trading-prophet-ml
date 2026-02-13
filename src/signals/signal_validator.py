"""Signal validation utilities."""
from __future__ import annotations

import pandas as pd


def filter_low_confidence(df: pd.DataFrame, min_confidence: float) -> pd.DataFrame:
    out = df.copy()
    if "confidence" in out:
        out.loc[out["confidence"] < min_confidence, "signal"] = "HOLD"
    return out


def confirm_multi_timeframe(df_fast: pd.DataFrame, df_slow: pd.DataFrame) -> pd.DataFrame:
    out = df_fast.copy()
    out["confirmed"] = (df_fast["signal"] == df_slow.reindex(df_fast.index)["signal"]).fillna(False)
    return out


def validate_risk_reward(df: pd.DataFrame, min_rr: float) -> pd.DataFrame:
    out = df.copy()
    out["rr_valid"] = True
    if "risk_reward" in out:
        out["rr_valid"] = out["risk_reward"] >= min_rr
    return out
