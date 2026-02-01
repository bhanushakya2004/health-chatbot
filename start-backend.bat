@echo off
echo ========================================
echo Starting Health Chatbot - Backend
echo ========================================
echo.

cd healthcare-api

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Setting up virtual environment...
if not exist ".venv" (
    echo Creating new virtual environment with UV...
    uv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        echo Please install UV: pip install uv
        pause
        exit /b 1
    )
)

echo.
echo Installing/Updating dependencies...
uv pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Try running: setup-backend-fresh.bat
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting FastAPI server on port 8000...
echo ========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo NOTE: Make sure MongoDB is running!
echo Start MongoDB with: mongod
echo.

.venv\Scripts\python.exe -m uvicorn app.main:app --reload

pause
