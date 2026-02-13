"""Chart plotting utilities."""
from __future__ import annotations

import pandas as pd


def plot_candles(df: pd.DataFrame) -> None:
    try:
        import mplfinance as mpf
    except ImportError:  # pragma: no cover
        return
    mpf.plot(df, type="candle", volume=True, style="yahoo")


def plot_signals(df: pd.DataFrame) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # pragma: no cover
        return
    plt.plot(df.index, df["close"], label="Close")
    buys = df[df["signal"] == "BUY"]
    sells = df[df["signal"] == "SELL"]
    plt.scatter(buys.index, buys["close"], marker="^", color="green")
    plt.scatter(sells.index, sells["close"], marker="v", color="red")
    plt.legend()
    plt.show()
