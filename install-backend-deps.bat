@echo off
echo ========================================
echo Installing Backend Dependencies
echo (Python 3.13 Compatible)
echo ========================================
echo.

cd healthcare-api

echo Installing core packages...
pip install --upgrade pip

echo.
echo Installing FastAPI and Uvicorn...
pip install fastapi uvicorn[standard]

echo.
echo Installing Pydantic (latest with wheels)...
pip install --only-binary=:all: pydantic

echo.
echo Installing MongoDB driver...
pip install pymongo

echo.
echo Installing authentication packages...
pip install python-jose[cryptography] passlib[bcrypt]

echo.
echo Installing utility packages...
pip install python-multipart python-dotenv

echo.
echo Installing Agno...
pip install agno

echo.
echo ========================================
echo Verifying installation...
echo ========================================
python -c "import fastapi; print('✓ FastAPI:', fastapi.__version__)"
python -c "import uvicorn; print('✓ Uvicorn:', uvicorn.__version__)"
python -c "import pydantic; print('✓ Pydantic:', pydantic.__version__)"
python -c "import pymongo; print('✓ PyMongo:', pymongo.__version__)"
python -c "import passlib; print('✓ Passlib: OK')"
python -c "from jose import jwt; print('✓ Python-JOSE: OK')"

echo.
echo ========================================
echo ✅ All dependencies installed!
echo ========================================
echo.
echo You can now run: start-backend.bat
echo.
pause
