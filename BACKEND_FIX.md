# Backend Startup Error Fix

## Error: `ModuleNotFoundError: No module named 'pymongo'`

This error means Python dependencies are not installed properly.

## Quick Fix

### Option 1: Use the Regular Startup Script (Recommended)
```bash
# Close the current backend terminal (Ctrl+C)
# Run this instead:
start-backend.bat
```

This will install all dependencies with pip.

### Option 2: Manual Install
```bash
cd healthcare-api
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Option 3: Install Individual Package
```bash
pip install pymongo
```

## Why This Happened

The `uv` package manager didn't install the dependencies correctly. The script has been updated to use regular `pip` which is more reliable.

## Updated Scripts

**start-backend.bat** - Uses regular pip (reliable) ✅
**start-backend-uv.bat** - Uses uv with --system flag (optional, faster)

## Full Setup Steps

### 1. Make sure MongoDB is running
```bash
mongod
```

### 2. Install dependencies
```bash
cd healthcare-api
pip install -r requirements.txt
```

### 3. Seed database (first time only)
```bash
cd ..
seed-database.bat
```

### 4. Start backend
```bash
start-backend.bat
```

### 5. Start frontend (new terminal)
```bash
start-frontend.bat
```

## Verify Installation

Check if all packages are installed:
```bash
cd healthcare-api
pip list | findstr pymongo
pip list | findstr fastapi
pip list | findstr uvicorn
```

Should show:
```
fastapi      0.109.0
pymongo      4.6.1
uvicorn      0.27.0
```

## Alternative: Use Virtual Environment

For cleaner dependency management:

```bash
cd healthcare-api

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --reload
```

## Still Having Issues?

### Check Python Version
```bash
python --version
```
Should be Python 3.8 or higher

### Reinstall All Dependencies
```bash
cd healthcare-api
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Check MongoDB
Make sure MongoDB is running:
```bash
mongod
```

Should see:
```
[initandlisten] waiting for connections on port 27017
```

## Success Indicators

When backend starts correctly, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ Connected to MongoDB
```

No errors about missing modules!

## Next Step After Fix

Once backend is running properly:
1. Go to http://localhost:8000/docs - Should see API documentation
2. Go to http://localhost:8000/health - Should see `{"status":"healthy"}`
3. Start frontend with `start-frontend.bat`
4. Open http://localhost:5173 and login!

---

**Fixed Script Location**: `start-backend.bat`
**Backup Script**: `start-backend-uv.bat` (uses uv, experimental)
