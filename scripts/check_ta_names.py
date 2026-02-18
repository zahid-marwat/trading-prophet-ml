
import pandas as pd
import pandas_ta as ta

df = pd.DataFrame({
    "close": [100.0] * 50,
    "high": [105.0] * 50,
    "low": [95.0] * 50,
    "open": [100.0] * 50,
    "volume": [1000] * 50
})

try:
    # Test SMA
    sma = ta.sma(df["close"], length=20)
    print(f"SMA name: {sma.name}")

    # Test MACD
    macd = ta.macd(df["close"])
    print(f"MACD columns: {macd.columns.tolist()}")

    # Test RSI
    rsi = ta.rsi(df["close"], length=14)
    print(f"RSI name: {rsi.name}")

    # Test Bollinger Bands
    bb = ta.bbands(df["close"])
    print(f"BB lines: {bb.columns.tolist()}")

except Exception as e:
    print(e)
