# Health Chatbot - Quick Start Guide

## Prerequisites

### Required Software
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download](https://nodejs.org/)
3. **MongoDB** - [Download](https://www.mongodb.com/try/download/community)

### Check Installations
```bash
python --version
node --version
npm --version
mongod --version
```

## Quick Start (Windows)

### Option 1: Using Batch Scripts (Easiest)

1. **Start MongoDB** (in a separate terminal):
   ```bash
   mongod
   ```

2. **Seed Database** (first time only - creates test users):
   ```bash
   seed-database.bat
   ```
   This creates 5 test users with sample data. See [CREDENTIALS.md](CREDENTIALS.md) for login details.

3. **Start Backend** (double-click or run):
   ```bash
   start-backend.bat
   ```
   Backend will run at: http://localhost:8000
   API Docs: http://localhost:8000/docs

4. **Start Frontend** (in a new terminal, double-click or run):
   ```bash
   start-frontend.bat
   ```
   Frontend will run at: http://localhost:5173

### Option 2: Manual Start

#### 1. Start MongoDB
```bash
mongod
```

#### 2. Seed Database (first time only)
```bash
cd healthcare-api
python seed_database.py
```

#### 3. Start Backend
```bash
cd healthcare-api
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### 4. Start Frontend
```bash
cd medicare-chat
npm install
npm run dev
```

## Quick Start (Linux/Mac)

### 1. Start MongoDB
```bash
mongod
```

### 2. Seed Database (first time only)
```bash
cd healthcare-api
python seed_database.py
```

### 3. Start Backend
```bash
cd healthcare-api
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 4. Start Frontend
```bash
cd medicare-chat
npm install
npm run dev
```

## First Time Setup

### 1. Configure Backend
Create/Edit `healthcare-api/.env`:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=healthcare_db
SECRET_KEY=your-secret-key-here-change-in-production
```

### 2. Configure Frontend
Create/Edit `medicare-chat/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Using the Application

### 1. Sign Up or Use Test Account

**Option A: Use Pre-created Test Account**
- Open http://localhost:5173
- Click "Sign in"
- Use credentials from [CREDENTIALS.md](CREDENTIALS.md):
  - Email: `test@example.com`
  - Password: `test123`

**Option B: Create New Account**
- Click "Sign up" in the sidebar
- Enter your details:
  - Full Name
  - Email
  - Password
- Click "Create account"

### 2. Chat with AI
- After login, click "New Chat"
- Type your health question
- Press Enter or click Send
- Wait for AI response

### 3. Logout
- Click "Log out" in the sidebar

## Troubleshooting

### MongoDB Connection Error
**Error**: "Failed to connect to MongoDB"
**Solution**: 
- Make sure MongoDB is running: `mongod`
- Check MongoDB URL in `.env` file
- Default: `mongodb://localhost:27017`

### Backend Port Already in Use
**Error**: "Address already in use: 8000"
**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Frontend Can't Connect to Backend
**Error**: "Network Error" or "Failed to fetch"
**Solution**:
- Verify backend is running: http://localhost:8000/health
- Check `.env` file has correct `VITE_API_BASE_URL`
- Check browser console for CORS errors

### CORS Errors
**Solution**: Backend already has CORS enabled for all origins. If issues persist:
- Clear browser cache
- Try incognito/private mode
- Check backend terminal for errors

### Module Not Found Errors
**Backend**:
```bash
cd healthcare-api
pip install -r requirements.txt
```

**Frontend**:
```bash
cd medicare-chat
npm install
```

## API Endpoints

### Authentication
- **POST** `/signup` - Create new user account
- **POST** `/login` - Login (returns JWT token)

### Chat
- **POST** `/healthchat` - Send message to AI (requires auth)

### Health Check
- **GET** `/health` - Check if backend is running
- **GET** `/` - API information

## Environment Variables

### Backend (healthcare-api/.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=healthcare_db
SECRET_KEY=your-secret-key-here-change-in-production
```

### Frontend (medicare-chat/.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Test Credentials

After running `seed-database.bat`, you'll have 5 pre-created accounts.
See [CREDENTIALS.md](CREDENTIALS.md) for complete list.

**Quick Test Account:**
- Email: `test@example.com`
- Password: `test123`

**Doctor Account (with patient data):**
- Email: `doctor@medihelp.com`
- Password: `doctor123`

## Development URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React app |
| Backend | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| MongoDB | mongodb://localhost:27017 | Database |

## Project Structure

```
health-chatbot/
├── healthcare-api/          # Backend (FastAPI)
│   ├── app/
│   │   ├── routes/         # API routes
│   │   ├── models/         # Data models
│   │   ├── config/         # Configuration
│   │   └── main.py         # Main application
│   ├── requirements.txt
│   └── .env
│
├── medicare-chat/          # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # API services
│   │   ├── hooks/        # Custom hooks
│   │   └── pages/        # Page components
│   ├── package.json
│   └── .env
│
└── INTEGRATION_GUIDE.md   # Detailed integration docs
```

## Need Help?

1. Check API documentation: http://localhost:8000/docs
2. Review INTEGRATION_GUIDE.md for detailed technical docs
3. Check browser console for frontend errors
4. Check terminal output for backend errors

## Next Steps

After successful setup:
1. ✅ Test authentication (signup/login/logout)
2. ✅ Test chat functionality
3. 📝 Add more AI features
4. 📝 Implement chat history persistence
5. 📝 Add file upload for medical records
