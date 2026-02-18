
import pandas_ta as ta
try:
    print(f"ta.cdl_hammer exists: {hasattr(ta, 'cdl_hammer')}")
    print(f"ta.hammer exists: {hasattr(ta, 'hammer')}")
    print(f"ta.cdl_pattern exists: {hasattr(ta, 'cdl_pattern')}")
    print(f"Attributes starting with cdl_: {[a for a in dir(ta) if a.startswith('cdl_')]}")
except Exception as e:
    print(e)
