import pandas as pd
from src.backtesting.backtester import run_backtest


def test_run_backtest() -> None:
    df = pd.DataFrame(
        {
            "close": [100, 101, 102, 101],
            "signal": ["HOLD", "BUY", "HOLD", "SELL"],
        }
    )
    df.index = pd.date_range("2020-01-01", periods=len(df))
    result = run_backtest(df)
    assert not result.equity_curve.empty
