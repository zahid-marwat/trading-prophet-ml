# Trading Prophet ML

## Overview
Trading Prophet ML is a research-grade stock and cryptocurrency prediction system featuring multi-source data ingestion, technical indicators, pattern recognition, ML/DL modeling, signal generation, and robust backtesting. It is designed to provide **decision support** with transparent uncertainty and risk metrics.

## Key Features
- Multi-asset support (stocks, crypto, indices)
- Multi-timeframe data pipeline (1m to 1d)
- Technical indicators and feature engineering
- Automated candlestick and chart pattern recognition
- Baseline ML, classical time-series, and deep learning models
- Signal generation with confidence, risk-reward, and validation filters
- Realistic backtesting (fees, slippage, and position management)
- Risk management and position sizing tools
- Streamlit dashboard and FastAPI endpoints

## Supported Assets
- Stocks: AAPL, GOOGL, TSLA, MSFT, etc.
- Crypto: BTC, ETH, ADA, SOL, etc.
- Indices: S&P 500, NASDAQ
- Custom tickers and exchanges supported via configuration

## Prediction Models
- Baseline: Linear Regression, Random Forest, XGBoost, SVR
- Time-series: ARIMA/SARIMA, Prophet, Exponential Smoothing
- Deep Learning: LSTM, GRU, BiLSTM, CNN-LSTM, Transformer (TFT)
- Ensembles: Weighted, stacking, regime-based selection

## Strategies
- Trend Following
- Mean Reversion
- Breakout
- Pattern-Based
- ML Prediction
- Hybrid strategies combining multiple approaches

## Setup & Installation
1. Create a virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill API keys
4. Review [config/config.yaml](config/config.yaml) and [config/trading_parameters.yaml](config/trading_parameters.yaml)

## API Usage
Start API:
- `uvicorn api.main:app --reload`

Endpoints:
- `POST /predict`
- `GET /signals`
- `GET /patterns`
- `GET /backtest`
- `POST /analyze`
- WebSocket `/ws`

## Backtesting Results
Backtest outputs are stored in results/. Metrics include total/annualized return, Sharpe/Sortino, max drawdown, win rate, and risk-reward. All results must include transaction costs and slippage assumptions.

## PROMINENT FINANCIAL DISCLAIMER
**This project is for educational and research purposes only. It does not constitute financial advice, investment recommendations, or a solicitation to buy or sell any securities or digital assets.** Trading involves substantial risk and may result in significant losses. See [FINANCIAL_DISCLAIMER.md](FINANCIAL_DISCLAIMER.md).

## Risk Warnings and Limitations
- Past performance does not guarantee future results.
- Model outputs are probabilistic and can be wrong.
- Backtests may overfit; forward testing is required.
- Liquidity, slippage, and fees materially impact results.
- Market regimes can shift abruptly and invalidate models.

## License
See [LICENSE](LICENSE).
