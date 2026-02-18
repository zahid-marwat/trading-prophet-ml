
import sys
import os
from pathlib import Path

# Ensure project root is in python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.service import analyze_asset

if __name__ == "__main__":
    print(f"Testing Analysis for: BTC/USDT")
    try:
        analysis = analyze_asset("BTC/USDT", "1d")
        if "error" in analysis:
            print(f"❌ Analysis Result Error: {analysis['error']}")
        else:
            print(f"✅ Analysis Successful. Rows: {analysis.get('rows')}")
    except Exception as e:
        print(f"❌ CRITICAL EXCEPTION: {e}")
