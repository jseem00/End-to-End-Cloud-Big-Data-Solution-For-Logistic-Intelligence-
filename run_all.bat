@echo off
echo =======================================================
echo 🚀 LOGISTICS INTELLIGENCE PIPELINE ^& DASHBOARD
echo =======================================================
echo.

:: Set encoding to support emojis in python print statements
set PYTHONIOENCODING=utf-8

:: 1. Run Pipeline
echo [1/2] Running Complete Pipeline (Data Generation, ETL, ML)...
python run_pipeline.py --mode simple
if %errorlevel% neq 0 (
    echo ❌ Pipeline execution failed.
    pause
    exit /b %errorlevel%
)

:: 2. Run Dashboard
echo.
echo [2/2] Launching Interactive Dashboard...
echo The dashboard will open in your default web browser shortly.
python -m streamlit run step4-deployment\dashboard.py

pause
