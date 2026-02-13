"""Dashboard component helpers."""
from __future__ import annotations

import pandas as pd


def equity_curve_component(equity: pd.Series) -> dict:
    return {"equity": equity.to_list()}
