import pandas as pd
from src.features.technical_indicators import add_indicators


def test_add_indicators_runs() -> None:
    df = pd.DataFrame(
        {
            "open": [1, 2, 3],
            "high": [2, 3, 4],
            "low": [0.5, 1.5, 2.5],
            "close": [1.5, 2.5, 3.5],
            "volume": [100, 120, 130],
        }
    )
    out = add_indicators(df)
    assert len(out) == len(df)
