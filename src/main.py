"""CLI entrypoint."""
from __future__ import annotations

import argparse

from .logging_config import configure_logging
from .pipeline import run_quick_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Trading Prophet ML")
    parser.add_argument("--asset", required=True, help="Ticker or symbol, e.g., AAPL or BTC/USDT")
    parser.add_argument("--timeframe", default="1d")
    parser.add_argument("--period", default="1y")
    args = parser.parse_args()

    configure_logging()
    result = run_quick_analysis(args.asset, args.timeframe, args.period)
    print(result)


if __name__ == "__main__":
    main()
