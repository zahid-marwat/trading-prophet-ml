import pandas as pd
from src.models.baseline_models import build_baseline_models


def test_build_baseline_models() -> None:
    models = build_baseline_models()
    assert models.linear is not None
    assert models.random_forest is not None
    assert models.svr is not None


def test_predict_shape() -> None:
    X = pd.DataFrame({"x": [1, 2, 3, 4]})
    y = pd.Series([1, 2, 3, 4])
    model = build_baseline_models().linear
    model.fit(X, y)
    preds = model.predict(X)
    assert len(preds) == len(X)
