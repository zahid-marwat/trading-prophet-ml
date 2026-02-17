"""Streamlit dashboard for Trading Prophet ML."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from dashboard.assets import STOCKS, CRYPTO, FOREX
from src.service import analyze_asset, predict_asset


# Custom layout configuration
st.set_page_config(
    page_title="Trading Prophet ML",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=300)
def cached_analysis(asset: str, timeframe: str) -> dict:
    try:
        return analyze_asset(asset, timeframe)
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=300)
def cached_prediction(asset: str, timeframe: str) -> dict:
    try:
        return predict_asset(asset, timeframe)
    except Exception as e:
        return {"error": str(e)}


def main():
    # Header Layout with Theme Toggle on the Right
    header_col, theme_col = st.columns([0.85, 0.15])
    
    with header_col:
        st.markdown('<div class="main-header">Trading Prophet ML 🚀</div>', unsafe_allow_html=True)
        
    with theme_col:
        st.write("") # Spacer
        theme_mode = st.selectbox("Theme", ["Dark 🌙", "Light ☀️"], index=0, label_visibility="collapsed")
    
    is_dark = "Dark" in theme_mode

    # Define Colors based on theme
    if is_dark:
        bg_color = "#0E1117"
        text_color = "#FAFAFA"
        card_bg = "#1E2130"
        metric_label = "#B0BEC5"
        metric_value_color = "#00E5FF" # Cyan for Dark Mode
        plotly_template = "plotly_dark"
    else:
        bg_color = "#FFFFFF"
        text_color = "#000000"       # Pure Black for max contrast
        card_bg = "#F0F2F6"          # Light Grey Card
        metric_label = "#333333"     # Dark Grey Label
        metric_value_color = "#0068C9" # Streamlit Blue for Light Mode (High Contrast)
        plotly_template = "plotly_white"

    # Inject Dynamic CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .main-header {{
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            font-size: 3rem;
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            background-color: {card_bg};
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: {metric_value_color};
        }}
        .metric-label {{
            font-size: 0.9rem;
            color: {metric_label};
        }}
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### ⚙️ Asset Configuration")
    
    asset_type = st.sidebar.radio("Asset Class", ["Stocks", "Crypto", "Forex", "Custom"])
    
    if asset_type == "Stocks":
        asset = st.sidebar.selectbox("Select Asset", STOCKS, index=0)
    elif asset_type == "Crypto":
        asset = st.sidebar.selectbox("Select Pair", CRYPTO, index=0)
    elif asset_type == "Forex":
        asset = st.sidebar.selectbox("Select Pair", FOREX, index=0)
    else:  # Custom
        asset = st.sidebar.text_input("Asset Symbol (yfinance/ccxt)", "NVDA")

    timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d", "1wk"], index=5)
    
    st.sidebar.markdown("### 🛠️ Chart Settings")
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    
    st.sidebar.markdown("**Overlays**")
    show_sma = st.sidebar.checkbox("SMA 20", value=True)
    show_ema = st.sidebar.checkbox("EMA 20", value=False)
    show_bb = st.sidebar.checkbox("Bollinger Bands", value=False)
    
    st.sidebar.markdown("**Oscillators**")
    show_rsi = st.sidebar.checkbox("RSI 14", value=False)
    show_macd = st.sidebar.checkbox("MACD", value=False)

    # Helper for custom metric cards
    def custom_metric(label, value, delta=None, color_trend=True):
        delta_html = ""
        if delta:
            # Parse delta to determine color
            delta_val = float(delta.strip('%').replace('+', ''))
            color = "#00FF00" if delta_val > 0 else "#FF0000"
            arrow = "↑" if delta_val > 0 else "↓"
            delta_html = f'<span style="color: {color}; font-size: 1rem; margin-left: 10px;">{arrow} {delta}</span>'
        
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">
                {value}
                {delta_html}
            </div>
        </div>
        """

    if st.sidebar.button("Run Analysis", type="primary", use_container_width=True):
        with st.spinner(f"Fetching data and analyzing {asset}..."):
            analysis = cached_analysis(asset, timeframe)
            prediction = cached_prediction(asset, timeframe)

        if "error" in analysis:
            st.error(f"Analysis failed: {analysis['error']}")
            return
        
        if "error" in prediction:
            st.error(f"Prediction failed: {prediction['error']}")
            return

        # Main Dashboard Layout
        
        # 1. Key Metrics Row
        if "history" in analysis:
            df = pd.DataFrame(analysis["history"])
            if not df.empty:
                last_close = df.iloc[-1]["close"]
                prev_close = df.iloc[-2]["close"]
                high_24h = df["high"].iloc[-24:].max() if len(df) >= 24 else df["high"].max()
                low_24h = df["low"].iloc[-24:].min() if len(df) >= 24 else df["low"].max()
                volume_24h = df["volume"].iloc[-24:].sum() if len(df) >= 24 else df["volume"].sum()
                
                change_pct = (last_close - prev_close) / prev_close * 100
                
                # Top Row: Signal & Price
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    st.markdown(custom_metric("Current Price", f"${last_close:,.2f}", f"{change_pct:+.2f}%"), unsafe_allow_html=True)
                
                with c2:
                    pred_price = prediction.get("prediction", 0)
                    pred_pct = (pred_price - last_close) / last_close * 100
                    st.markdown(custom_metric("Predicted Price", f"${pred_price:,.2f}", f"{pred_pct:+.2f}%"), unsafe_allow_html=True)
                
                with c3:
                    trend = "Bullish 🐂" if pred_pct > 0 else "Bearish 🐻"
                    st.markdown(custom_metric("Signal", trend), unsafe_allow_html=True)
                    
                with c4:
                     st.markdown(custom_metric("Confidence", f"{prediction.get('confidence', 0):.2f}"), unsafe_allow_html=True)

                # Calculate Date Range
                if 'timestamp' in df.columns:
                    dates = pd.to_datetime(df['timestamp'])
                else:
                    dates = pd.to_datetime(df.index)
                
                start_date = dates.min().strftime('%Y-%m-%d %H:%M')
                end_date = dates.max().strftime('%Y-%m-%d %H:%M')

                st.markdown(f"**Data Range:** `{start_date}` to `{end_date}`")

                # Second Row: Market Stats
                st.markdown(f"**Period Stats ({timeframe})**")
                s1, s2, s3, s4 = st.columns(4)
                s1.markdown(custom_metric("Highest (Last 24)", f"${high_24h:,.2f}"), unsafe_allow_html=True)
                s2.markdown(custom_metric("Lowest (Last 24)", f"${low_24h:,.2f}"), unsafe_allow_html=True)
                s3.markdown(custom_metric("Total Volume", f"{volume_24h:,.0f}"), unsafe_allow_html=True)
                s4.markdown(custom_metric("RSI (14)", f"{df.iloc[-1].get('rsi_14', 0):.2f}"), unsafe_allow_html=True)

        st.markdown("---")

        # 2. Tabs for Charts & Details
        tab1, tab2, tab3 = st.tabs(["📊 Interactive Chart", "🧠 Analysis & Forecast", "📋 Raw Data"])

        with tab1:
            if "history" in analysis and not df.empty:
                # Dynamic Subplots
                rows = 1
                row_heights = [0.7]
                
                if show_volume:
                    rows += 1
                    row_heights = [0.6, 0.15] if rows == 2 else [0.5, 0.15, 0.15]
                if show_rsi:
                    rows += 1
                    row_heights.append(0.15)
                if show_macd:
                    rows += 1
                    row_heights.append(0.15)
                
                # Normalize heights
                total = sum(row_heights)
                row_heights = [h/total for h in row_heights]

                subplot_titles = [f'{asset} Price ({start_date} - {end_date})']
                if show_volume: subplot_titles.append('Volume')
                if show_rsi: subplot_titles.append('RSI (14)')
                if show_macd: subplot_titles.append('MACD')

                fig = make_subplots(
                    rows=rows, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.03, 
                    subplot_titles=subplot_titles, 
                    row_heights=row_heights
                )

                # 1. Candlestick (Main Chart)
                fig.add_trace(go.Candlestick(
                    x=df['timestamp'] if 'timestamp' in df.columns else df.index,
                    open=df['open'], high=df['high'], low=df['low'], close=df['close'],
                    name='OHLC'
                ), row=1, col=1)

                # Overlays
                if show_sma and 'sma_20' in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df['sma_20'], line=dict(color='orange', width=1), name='SMA 20'), row=1, col=1)
                if show_ema and 'ema_20' in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df['ema_20'], line=dict(color='blue', width=1), name='EMA 20'), row=1, col=1)
                if show_bb and 'bb_upper' in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df['bb_upper'], line=dict(color='gray', width=1, dash='dot'), name='BB Upper'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['bb_lower'], line=dict(color='gray', width=1, dash='dot'), name='BB Lower', fill='tonexty'), row=1, col=1)

                current_row = 2
                
                # 2. Volume
                if show_volume:
                    colors = ['red' if row['open'] - row['close'] >= 0 else 'green' for index, row in df.iterrows()]
                    fig.add_trace(go.Bar(
                        x=df['timestamp'] if 'timestamp' in df.columns else df.index,
                        y=df['volume'], marker_color=colors, showlegend=False, name='Volume'
                    ), row=current_row, col=1)
                    current_row += 1

                # 3. RSI
                if show_rsi and 'rsi_14' in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df['rsi_14'], line=dict(color='purple', width=1), name='RSI'), row=current_row, col=1)
                    fig.add_hline(y=70, line_dash="dash", line_color="red", row=current_row, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="green", row=current_row, col=1)
                    current_row += 1

                # 4. MACD
                if show_macd and 'macd' in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df['macd'], line=dict(color='blue', width=1), name='MACD'), row=current_row, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['macd_signal'], line=dict(color='orange', width=1), name='Signal'), row=current_row, col=1)
                    fig.add_trace(go.Bar(x=df.index, y=df['macd_hist'], name='Hist'), row=current_row, col=1)
                    current_row += 1

                fig.update_layout(
                    height=800 if rows > 2 else 600,
                    xaxis_rangeslider_visible=True,
                    xaxis_rangeslider_thickness=0.05,
                    template=plotly_template,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No historical data available for plotting.")

        with tab2:
            st.markdown("### 🤖 Model Findings")
            if "findings" in prediction:
                st.success(prediction['findings'])
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Performance Metrics")
                metrics = analysis.get("metrics", {})
                st.json(metrics)
            
            with col_b:
                st.markdown("#### Prediction Parameters")
                st.json({
                    "Method": prediction.get("method"),
                    "Horizon": "5 Steps",
                    "Window": "30 Periods"
                })

        with tab3:
            st.dataframe(df if "history" in analysis else pd.DataFrame())

    else:
        # Placeholder or Landing Page
        st.info("👈 Select an asset from the sidebar and click **Run Analysis** to start.")
        st.markdown("### Supported Assets")
        st.markdown(f"**Stocks:** {', '.join(STOCKS[:10])}...")
        st.markdown(f"**Crypto:** {', '.join(CRYPTO[:10])}...")

if __name__ == "__main__":
    main()
