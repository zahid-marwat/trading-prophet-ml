"""Sentiment feature generation (placeholders)."""
from __future__ import annotations

import pandas as pd


def add_sentiment_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["news_sentiment"] = pd.NA
    out["social_sentiment"] = pd.NA
    out["fear_greed"] = pd.NA
    return out
