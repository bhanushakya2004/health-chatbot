@echo off
echo ========================================
echo MongoDB Database Seeding
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
echo Checking MongoDB connection...
echo Make sure MongoDB is running (mongod)
echo.

echo Running seed script...
python seed_database.py

echo.
echo ========================================
echo Done!
echo ========================================
pause
