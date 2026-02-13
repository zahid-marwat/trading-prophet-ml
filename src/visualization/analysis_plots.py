"""Analysis plots."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_equity_curve(equity: pd.Series) -> None:
    plt.plot(equity.index, equity.values)
    plt.title("Equity Curve")
    plt.show()


def plot_drawdown(equity: pd.Series) -> None:
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1
    plt.plot(drawdown.index, drawdown.values)
    plt.title("Drawdown")
    plt.show()
