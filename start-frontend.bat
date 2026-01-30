@echo off
echo ========================================
echo Starting Health Chatbot - Frontend
echo ========================================
echo.

cd medicare-chat

echo Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Vite development server...
echo ========================================
echo.
echo Frontend will open at: http://localhost:5173
echo.

call npm run dev

pause
