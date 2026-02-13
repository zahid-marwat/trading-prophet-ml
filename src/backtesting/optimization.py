"""Optimization utilities (placeholder)."""
from __future__ import annotations

from typing import Callable


def grid_search(params: dict, objective: Callable[..., float]) -> dict:
    best_score = float("-inf")
    best_params = {}
    for key, values in params.items():
        for value in values:
            score = objective(**{key: value})
            if score > best_score:
                best_score = score
                best_params = {key: value}
    return {"best_score": best_score, "best_params": best_params}
