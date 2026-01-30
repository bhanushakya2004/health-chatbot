@echo off
echo ========================================
echo Quick Fix for Python 3.13 Dependencies
echo ========================================
echo.

cd healthcare-api

echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing with pre-built wheels only (no compilation)...
pip install --only-binary=:all: fastapi==0.109.0 uvicorn==0.27.0 2>nul
if %errorlevel% neq 0 (
    echo Installing FastAPI without version constraint...
    pip install fastapi uvicorn[standard]
)

pip install --only-binary=:all: pydantic 2>nul
if %errorlevel% neq 0 (
    echo Installing latest Pydantic...
    pip install pydantic
)

pip install --only-binary=:all: pymongo 2>nul
if %errorlevel% neq 0 (
    echo Installing PyMongo...
    pip install pymongo
)

echo.
echo Installing bcrypt (compatible version)...
pip install bcrypt==4.1.2 2>nul
if %errorlevel% neq 0 (
    echo Installing latest bcrypt...
    pip install bcrypt
)

echo.
echo Installing remaining packages...
pip install python-multipart python-dotenv python-jose[cryptography] passlib agno

echo.
echo ========================================
echo Testing imports...
echo ========================================
python -c "import fastapi, uvicorn, pydantic, pymongo; print('✅ All core packages imported successfully!')"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Some packages failed to import
    echo Try manually: pip install fastapi uvicorn pydantic pymongo
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Installation complete!
echo ========================================
echo.
echo Run: start-backend-fast.bat
echo.
pause
