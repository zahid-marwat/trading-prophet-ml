"""FastAPI app for Trading Prophet ML."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from .models_endpoints import router as models_router
from src.service import analyze_asset, predict_asset

app = FastAPI(title="Trading Prophet ML", version="0.1.0")
app.include_router(models_router)


class PredictRequest(BaseModel):
    asset: str
    timeframe: str = "1d"
    horizon: int = 5


@app.get("/signals")
def get_signals() -> dict:
    results_dir = Path("results")
    if not results_dir.exists():
        return {"disclaimer": "Not financial advice.", "signals": [], "source": None}

    files = sorted(results_dir.glob("signals_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return {"disclaimer": "Not financial advice.", "signals": [], "source": None}

    latest = files[0]
    df = pd.read_csv(latest)
    tail = df.tail(100).to_dict(orient="records")
    return {
        "disclaimer": "Not financial advice.",
        "signals": tail,
        "source": latest.name,
    }


@app.get("/patterns")
def get_patterns() -> dict:
    return {"disclaimer": "Not financial advice.", "patterns": []}


@app.get("/backtest")
def run_backtest() -> dict:
    return {"disclaimer": "Not financial advice.", "results": {}}


@app.post("/predict")
def predict(req: PredictRequest) -> dict:
    pred = predict_asset(req.asset, req.timeframe, horizon=req.horizon)
    return {
        "disclaimer": "Not financial advice.",
        "asset": req.asset,
        "timeframe": req.timeframe,
        "horizon": req.horizon,
        "prediction": pred["prediction"],
        "confidence": pred["confidence"],
        "method": pred["method"],
        "findings": pred["findings"],
    }


@app.post("/analyze")
def analyze(req: PredictRequest) -> dict:
    analysis = analyze_asset(req.asset, req.timeframe)
    return {
        "disclaimer": "Not financial advice.",
        "asset": req.asset,
        "timeframe": req.timeframe,
        "analysis": analysis,
    }


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    await ws.send_json({"message": "Real-time stream placeholder."})
    await ws.close()
