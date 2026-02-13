"""Configuration loading utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    load_dotenv()
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
