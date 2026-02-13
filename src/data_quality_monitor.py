"""Data quality monitoring utilities."""
from __future__ import annotations

import pandas as pd


def check_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["anomaly"] = out["close"].pct_change().abs() > 0.2
    return out


def validate_api_connection(status: bool) -> bool:
    return status
