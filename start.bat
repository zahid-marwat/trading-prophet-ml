@echo off
set PYTHON_EXE="C:\Users\z-pc\AppData\Local\miniconda3\python.exe"

echo Starting Trading Prophet ML System...

:: Launch Backend API in a new window
echo Launching Backend API (FastAPI)...
start "Trading Prophet Backend" cmd /k %PYTHON_EXE% -m uvicorn api.main:app --reload

:: Wait a moment for backend to initialize
timeout /t 5 /nobreak >nul

:: Launch Frontend Dashboard in a new window
echo Launching Frontend Dashboard (Streamlit)...
start "Trading Prophet Dashboard" cmd /k %PYTHON_EXE% -m streamlit run dashboard/streamlit_app.py

echo All services launched!
