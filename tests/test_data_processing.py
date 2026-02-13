import pandas as pd
from src.data.data_preprocessor import handle_missing, normalize


def test_handle_missing() -> None:
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    out = handle_missing(df)
    assert out.isna().sum().sum() == 0


def test_normalize() -> None:
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    out = normalize(df)
    assert out.shape == df.shape
