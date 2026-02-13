"""Position sizing utilities."""
from __future__ import annotations

import numpy as np


def fixed_fractional(capital: float, fraction: float) -> float:
    return capital * fraction


def kelly_criterion(win_rate: float, win_loss_ratio: float) -> float:
    return max(0.0, win_rate - (1 - win_rate) / win_loss_ratio)


def volatility_based(capital: float, volatility: float, target_vol: float = 0.02) -> float:
    if volatility <= 0:
        return 0.0
    return capital * min(1.0, target_vol / volatility)


def risk_parity(weights: np.ndarray) -> np.ndarray:
    inv = 1.0 / weights
    return inv / inv.sum()
