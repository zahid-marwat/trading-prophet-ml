
import sys
import os
from src.service import analyze_asset

# Ensure src is in python path
sys.path.append(os.getcwd())

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
