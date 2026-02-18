
import sys
import os
from pathlib import Path
import pandas as pd
from pprint import pprint

# Ensure project root is in python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.service import analyze_asset, predict_asset

def test_flow(asset, timeframe):
    print(f"\n{'='*50}")
    print(f"Testing Analysis for: {asset} ({timeframe})")
    print(f"{'='*50}")

    try:
        # 1. Test Analysis
        print("Running analyze_asset...")
        analysis = analyze_asset(asset, timeframe)
        
        if "error" in analysis:
            print(f"❌ Analysis Result Error: {analysis['error']}")
            return

        rows = analysis.get("rows", 0)
        history = analysis.get("history", [])
        metrics = analysis.get("metrics", {})
        
        print(f"✅ Analysis Successful")
        print(f"   - Rows processed: {rows}")
        print(f"   - History length: {len(history)}")
        print(f"   - Metrics keys: {list(metrics.keys())}")
        
        # Check for critical columns in history for charting
        if len(history) > 0:
            sample = history[0]
            required_cols = ['open', 'high', 'low', 'close', 'volume', 'sma_20', 'ema_20', 'rsi_14']
            missing = [c for c in required_cols if c not in sample]
            if missing:
                print(f"⚠️  Missing columns in history for charting: {missing}")
            else:
                print(f"✅ All charting columns present")

        # 2. Test Prediction
        print("\nRunning predict_asset...")
        prediction = predict_asset(asset, timeframe)
        
        if "error" in prediction:
             print(f"❌ Prediction Result Error: {prediction['error']}")
             return

        print(f"✅ Prediction Successful")
        print(f"   - Predicted Price: {prediction.get('prediction')}")
        print(f"   - Confidence: {prediction.get('confidence')}")
        print(f"   - Findings: {prediction.get('findings')[:100]}...")

    except Exception as e:
        print(f"❌ CRITICAL EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test Stock
    test_flow("AAPL", "1d")
    
    # Test Crypto
    test_flow("BTC/USDT", "1d")
