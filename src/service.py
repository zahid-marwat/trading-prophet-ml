"""Service layer for API and dashboard."""
from __future__ import annotations

from typing import Any

from .data.data_fetcher import DataFetcher
from .data.data_manager import DataManager
from .data.data_preprocessor import adjust_for_splits_dividends, handle_missing
from .pipeline import run_quick_analysis
from .predictor import naive_linear_forecast


def analyze_asset(asset: str, timeframe: str = "1d", period: str = "1y") -> dict[str, Any]:
    return run_quick_analysis(asset=asset, timeframe=timeframe, period=period)


def predict_asset(asset: str, timeframe: str = "1d", period: str = "1y", horizon: int = 1) -> dict[str, Any]:
    fetcher = DataFetcher()
    manager = DataManager("data")
    cache_key = f"{asset}-{timeframe}-{period}"

    def _fetch():
        if "/" in asset:
            return fetcher.fetch_ccxt("binance", asset, timeframe)
        return fetcher.fetch_yfinance(asset, interval=timeframe, period=period)

    df = manager.get_or_fetch(cache_key, _fetch)
    df = adjust_for_splits_dividends(df)
    df = handle_missing(df)

    result = naive_linear_forecast(df, horizon=horizon)
    return {
        "prediction": result.prediction,
        "confidence": result.confidence,
        "method": result.method,
        "disclaimer": "Not financial advice.",
    }
