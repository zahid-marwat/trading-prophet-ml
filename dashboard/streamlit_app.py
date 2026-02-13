"""Streamlit dashboard for Trading Prophet ML."""
from __future__ import annotations

import streamlit as st

from src.service import analyze_asset, predict_asset


@st.cache_data(ttl=300)
def cached_analysis(asset: str, timeframe: str) -> dict:
	return analyze_asset(asset, timeframe)


@st.cache_data(ttl=300)
def cached_prediction(asset: str, timeframe: str) -> dict:
	return predict_asset(asset, timeframe)


st.set_page_config(page_title="Trading Prophet ML", layout="wide")

st.title("Trading Prophet ML Dashboard")
st.warning("Not financial advice. Use at your own risk.")

st.sidebar.header("Configuration")
asset = st.sidebar.text_input("Asset (e.g., AAPL or BTC/USDT)", "AAPL")
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=5)

st.subheader("Overview")
st.write(f"Selected asset: {asset}")
st.write(f"Timeframe: {timeframe}")

if st.button("Run Analysis"):
	analysis = cached_analysis(asset, timeframe)
	st.subheader("Analysis Metrics")
	st.json(analysis.get("metrics", {}))

	st.subheader("Prediction")
	prediction = cached_prediction(asset, timeframe)
	st.json(prediction)

st.subheader("Signals")
st.info("Signals are generated in the pipeline and stored in results/. Use the analysis output above.")

st.subheader("Backtesting")
st.info("Backtesting results placeholder. Integrate with src/backtesting.")
