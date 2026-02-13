"""End-to-end analysis pipeline."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from .config_loader import load_yaml
from .data.data_fetcher import DataFetcher
from .data.data_manager import DataManager
from .data.data_preprocessor import adjust_for_splits_dividends, handle_missing
from .features.feature_engineer import add_lags, add_market_regime, add_price_transforms, add_rolling_stats, add_time_features
from .features.technical_indicators import add_indicators
from .patterns.pattern_detector import detect_patterns
from .signals.signal_generator import generate_signals
from .backtesting.backtester import run_backtest
from .backtesting.performance_metrics import annualized_return, max_drawdown, sharpe_ratio, total_return

logger = logging.getLogger(__name__)


def _is_crypto(asset: str) -> bool:
    return "/" in asset


def run_quick_analysis(asset: str, timeframe: str = "1d", period: str = "1y") -> dict[str, Any]:
    """Run a minimal pipeline: fetch -> features -> patterns -> signals -> backtest."""
    config = load_yaml(Path("config") / "config.yaml")
    fetcher = DataFetcher()
    manager = DataManager(config.get("data", {}).get("cache_dir", "data"))

    cache_key = f"{asset}-{timeframe}-{period}"

    def _fetch() -> pd.DataFrame:
        if _is_crypto(asset):
            exchange = "binance"
            return fetcher.fetch_ccxt(exchange, asset, timeframe)
        return fetcher.fetch_yfinance(asset, interval=timeframe, period=period)

    df = manager.get_or_fetch(cache_key, _fetch)
    df = adjust_for_splits_dividends(df)
    df = handle_missing(df)

    df = add_indicators(df)
    df = add_price_transforms(df)
    df = add_lags(df)
    df = add_rolling_stats(df)
    df = add_time_features(df)
    df = add_market_regime(df)

    df = detect_patterns(df)
    df = generate_signals(df)

    bt = run_backtest(df)
    metrics = {
        "total_return": total_return(bt.equity_curve),
        "annualized_return": annualized_return(bt.equity_curve),
        "sharpe_ratio": sharpe_ratio(bt.equity_curve),
        "max_drawdown": max_drawdown(bt.equity_curve),
    }

    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    df.tail(200).to_csv(results_dir / f"signals_{asset.replace('/', '-')}_{stamp}.csv")
    bt.trades.to_csv(results_dir / f"trades_{asset.replace('/', '-')}_{stamp}.csv", index=False)

    return {
        "asset": asset,
        "timeframe": timeframe,
        "rows": len(df),
        "metrics": metrics,
        "disclaimer": "Not financial advice.",
    }
