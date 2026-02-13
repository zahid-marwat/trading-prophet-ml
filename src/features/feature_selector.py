"""Feature selection utilities."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression


def correlation_filter(df: pd.DataFrame, threshold: float = 0.9) -> pd.DataFrame:
    corr = df.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return df.drop(columns=to_drop, errors="ignore")


def recursive_feature_elimination(X: pd.DataFrame, y: pd.Series, n_features: int = 10) -> list[str]:
    model = LinearRegression()
    selector = RFE(model, n_features_to_select=n_features)
    selector = selector.fit(X, y)
    return list(X.columns[selector.support_])


def pca_reduce(X: pd.DataFrame, n_components: int = 5) -> pd.DataFrame:
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)
    return pd.DataFrame(components, index=X.index)
