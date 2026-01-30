# 🚀 Quick Start Guide - Health Chatbot

## ⚡ 3-Step Setup

### Step 1️⃣: Start MongoDB
```bash
mongod
```

### Step 2️⃣: Seed Database (First Time Only)
```bash
seed-database.bat
```
Creates 5 test users + sample data

### Step 3️⃣: Start Servers
```bash
# Terminal 1
start-backend.bat

# Terminal 2
start-frontend.bat
```

---

## 🔑 Test Credentials

| Account | Email | Password |
|---------|-------|----------|
| **Quick Test** | test@example.com | test123 |
| **Doctor** | doctor@medihelp.com | doctor123 |
| **Admin** | admin@medihelp.com | admin123 |

👉 See [CREDENTIALS.md](CREDENTIALS.md) for all accounts

---

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main app |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |

---

## 🧪 Quick Test

1. Go to http://localhost:5173
2. Login: `test@example.com` / `test123`
3. Click "New Chat"
4. Type: "What are symptoms of flu?"
5. Get AI response! 🎉

---

## 📁 Project Structure

```
health-chatbot/
├── start-backend.bat       ← Start backend
├── start-frontend.bat      ← Start frontend
├── seed-database.bat       ← Create test data
├── CREDENTIALS.md          ← All test accounts
├── README.md              ← Full documentation
├── healthcare-api/        ← Backend (FastAPI)
└── medicare-chat/         ← Frontend (React)
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| MongoDB error | Run `mongod` first |
| Backend won't start | Install deps: `cd healthcare-api && pip install -r requirements.txt` |
| Frontend won't start | Install deps: `cd medicare-chat && npm install` |
| Can't login | Run `seed-database.bat` to create users |
| CORS error | Make sure backend is running |

---

## 📚 Documentation

- **README.md** - Complete setup guide
- **CREDENTIALS.md** - All test accounts
- **INTEGRATION_GUIDE.md** - Technical details
- **ARCHITECTURE.md** - System design
- **TESTING_GUIDE.md** - Testing checklist

---

## ✨ Features

✅ JWT Authentication
✅ Protected Routes  
✅ AI Health Chat
✅ Real-time Responses
✅ Error Handling
✅ Dark/Light Mode

---

## 🔄 Reset Database

```bash
seed-database.bat
```
Clears old data and creates fresh sample data

---

## 📞 API Testing

### Login
```bash
curl -X POST http://localhost:8000/login \
  -F "username=test@example.com" \
  -F "password=test123"
```

### Chat (after login)
```bash
curl -X POST http://localhost:8000/healthchat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are flu symptoms?"}'
```

---

## 🎯 Next Steps

1. ✅ Start MongoDB
2. ✅ Seed database
3. ✅ Start backend
4. ✅ Start frontend
5. ✅ Login with test account
6. ✅ Try chat feature
7. 📝 Build more features!

---

**🎉 You're ready to go!**

Open http://localhost:5173 and start chatting!
