"""Model management endpoints placeholder."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def list_models() -> dict:
    return {"models": []}
