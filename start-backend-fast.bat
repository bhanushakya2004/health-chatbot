@echo off
echo ========================================
echo Starting Health Chatbot - Backend
echo (No dependency check)
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
echo If you get import errors, run: install-backend-deps.bat
echo.

python -m uvicorn app.main:app --reload

pause
