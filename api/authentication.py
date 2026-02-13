"""API key authentication utilities (optional)."""
from __future__ import annotations

from fastapi import Header, HTTPException


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
