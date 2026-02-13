"""Simple backtesting engine (placeholder)."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: pd.DataFrame


def run_backtest(df: pd.DataFrame, signal_col: str = "signal", fee_bps: float = 10, slippage_bps: float = 5) -> BacktestResult:
    equity = [1.0]
    trades = []
    position = 0
    for i in range(1, len(df)):
        signal = df.iloc[i][signal_col]
        price = df.iloc[i]["close"]
        if signal == "BUY" and position == 0:
            position = 1
            trades.append({"timestamp": df.index[i], "side": "BUY", "price": price})
        elif signal == "SELL" and position == 1:
            position = 0
            trades.append({"timestamp": df.index[i], "side": "SELL", "price": price})
        ret = df.iloc[i]["close"] / df.iloc[i - 1]["close"] - 1
        cost = (fee_bps + slippage_bps) / 10000.0
        equity.append(equity[-1] * (1 + ret - cost))
    return BacktestResult(pd.Series(equity, index=df.index), pd.DataFrame(trades))
