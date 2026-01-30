@echo off
echo ========================================
echo Starting Backend with UV (Fast Mode)
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
echo Checking uv installation...
uv --version
if %errorlevel% neq 0 (
    echo uv not found. Installing uv...
    pip install uv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install uv
        echo Please use start-backend.bat instead
        pause
        exit /b 1
    )
)

echo.
echo Installing dependencies with uv (fast)...
uv pip install -r requirements.txt --system
if %errorlevel% neq 0 (
    echo ERROR: uv install failed
    echo Try: start-backend.bat (uses regular pip)
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

python -m uvicorn app.main:app --reload

pause
