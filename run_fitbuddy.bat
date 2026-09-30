@echo off
title FitBuddy
cd /d "%~dp0"

if not exist ".env" (
    echo .env file not found. Copy .env.example to .env and add your GOOGLE_API_KEY.
    pause
    exit /b 1
)

if not exist "venv\Scripts\activate.bat" (
    echo First run: setting up environment, please wait...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:8000"
python -m uvicorn main:app
pause
