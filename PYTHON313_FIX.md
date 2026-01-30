# Python 3.13 Dependency Installation Fix

## Problem
Python 3.13.9 is very new, and `pydantic-core==2.14.6` doesn't have pre-built wheels for it yet. It tries to build from source, which requires Rust compiler.

## ✅ SOLUTION (Choose One)

### Option 1: Quick Fix Script (Recommended)
```bash
fix-backend-deps.bat
```
This installs only pre-built packages (no compilation needed).

### Option 2: Manual Installation
```bash
cd healthcare-api
pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic pymongo python-multipart python-dotenv python-jose[cryptography] passlib[bcrypt] agno
```

### Option 3: Use Python 3.11 or 3.12
If you have multiple Python versions:
```bash
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn app.main:app --reload
```

## 🚀 After Installing Dependencies

Once dependencies are installed, use the fast start script:
```bash
start-backend-fast.bat
```

This skips the installation check and just starts the server.

## 📋 Step-by-Step Guide

### 1. Fix Dependencies
```bash
fix-backend-deps.bat
```

Wait for it to complete. You should see:
```
✅ All core packages imported successfully!
✅ Installation complete!
```

### 2. Start MongoDB
Open a new terminal:
```bash
mongod
```

### 3. Seed Database (first time only)
```bash
seed-database.bat
```

### 4. Start Backend
```bash
start-backend-fast.bat
```

You should see:
```
✅ Connected to MongoDB
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 5. Start Frontend
Open a new terminal:
```bash
start-frontend.bat
```

### 6. Login
Go to http://localhost:5173
Login: test@example.com / test123

## 🔍 Verify Installation

Check if packages are installed:
```bash
cd healthcare-api
python -c "import fastapi, uvicorn, pydantic, pymongo; print('All OK!')"
```

Should print: `All OK!`

## 📦 Package Versions

After installation, you should have:
- fastapi: ~0.109.0 or newer
- uvicorn: ~0.27.0 or newer  
- pydantic: ~2.5.0 or newer (with pre-built wheels)
- pymongo: ~4.6.0 or newer
- python-jose, passlib, agno, etc.

## ❌ If Still Having Issues

### Issue: "No module named 'pydantic'"
```bash
pip install pydantic --force-reinstall
```

### Issue: "No module named 'pymongo'"
```bash
pip install pymongo
```

### Issue: "ModuleNotFoundError" for any package
```bash
pip install <package-name>
```

### Nuclear Option: Reinstall Everything
```bash
cd healthcare-api
pip uninstall -y fastapi uvicorn pydantic pymongo
pip install fastapi uvicorn[standard] pydantic pymongo python-multipart python-dotenv python-jose[cryptography] passlib[bcrypt] agno
```

## 🎯 Updated Scripts

| Script | Purpose |
|--------|---------|
| `fix-backend-deps.bat` | Install dependencies (smart, Python 3.13 compatible) |
| `start-backend-fast.bat` | Start server without dependency check |
| `start-backend.bat` | Start server with dependency check (may fail on 3.13) |
| `install-backend-deps.bat` | Alternative installer |

## 🔧 Why This Happens

- Python 3.13.9 was released recently (January 2026)
- Some packages don't have pre-compiled wheels for it yet
- `pydantic-core` tries to compile from source
- Compilation requires Rust toolchain (not usually on Windows)
- Using `--only-binary` or latest versions avoids this

## ✅ Success Indicators

When everything works:
1. ✅ `fix-backend-deps.bat` completes without errors
2. ✅ `python -c "import fastapi"` works
3. ✅ Backend starts: "Uvicorn running on http://127.0.0.1:8000"
4. ✅ Can open http://localhost:8000/docs
5. ✅ Can seed database
6. ✅ Frontend can connect and login

## 🎉 Next Steps

Once backend is running:
1. Open http://localhost:8000/docs - Test API
2. Run `seed-database.bat` - Create users
3. Run `start-frontend.bat` - Start UI
4. Login with test@example.com / test123
5. Start chatting! 💬

---

**TL;DR**: Run `fix-backend-deps.bat` then `start-backend-fast.bat`
