# 🏥 Healthcare AI Chatbot - Complete Project Knowledge

> **AI-Powered Health Consultation Platform with RAG, OCR, and Real-time Streaming**

This document contains comprehensive knowledge about the entire Healthcare AI Chatbot project, covering both frontend and backend architecture, implementation details, and usage instructions.

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Quick Start](#quick-start)
6. [Detailed Setup](#detailed-setup)
7. [Project Structure](#project-structure)
8. [Core Functionality](#core-functionality)
9. [API Reference](#api-reference)
10. [Development Guide](#development-guide)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

The Healthcare AI Chatbot is a full-stack application that provides intelligent health consultation through an AI agent powered by Google's Gemini model. The system features advanced capabilities including:

- **Real-time Streaming Responses** via Server-Sent Events
- **OCR Document Processing** for medical records
- **RAG (Retrieval-Augmented Generation)** for context-aware conversations
- **AI Health Summaries** generated from user data
- **Secure Authentication** with JWT tokens
- **Responsive Modern UI** built with React and Shadcn/ui

### Project Goals

1. Provide accessible health information through AI
2. Maintain context of user's medical history
3. Process and understand medical documents
4. Generate comprehensive health summaries
5. Deliver real-time conversational experience

---

## Key Features

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Real-time Chat** | Streaming responses using SSE | ✅ Complete |
| **OCR Processing** | Extract text from PDFs and images | ✅ Complete |
| **Health Summaries** | AI-generated health reports | ✅ Complete |
| **RAG System** | Context-aware document retrieval | ✅ Complete |
| **Document Management** | Upload, view, delete medical files | ✅ Complete |
| **User Profiles** | Age, gender, health data tracking | ✅ Complete |
| **Authentication** | JWT-based secure login | ✅ Complete |
| **Responsive Design** | Mobile and desktop support | ✅ Complete |

### 🎯 Advanced Capabilities

- **Agentic AI Architecture** using Agno framework
- **Vector Search** with ChromaDB for semantic matching
- **Background Processing** for OCR tasks
- **Session Persistence** with MongoDB
- **Memory Management** for conversation context
- **Tool Integration** (DuckDuckGo search)

---

## Tech Stack

### Backend

```
FastAPI (Python 3.9+)
├── AI & ML
│   ├── Agno Framework 0.0.25
│   ├── Google Gemini 2.0 Flash Exp
│   ├── ChromaDB 0.4.22 (Vector Store)
│   └── Tesseract OCR
├── Database
│   └── MongoDB with GridFS
├── Security
│   ├── JWT (python-jose)
│   ├── bcrypt
│   └── passlib
└── Document Processing
    ├── pytesseract 0.3.10
    ├── Pillow 10.2.0
    └── pdf2image 1.17.0
```

### Frontend

```
React 18.3.1 + TypeScript 5.6.2
├── Build Tool
│   └── Vite 6.0.1
├── UI Framework
│   ├── Shadcn/ui
│   ├── Radix UI
│   ├── Tailwind CSS 3.4.1
│   └── Lucide Icons
├── Routing
│   └── React Router DOM 7.1.1
└── Date Handling
    └── date-fns 4.1.0
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Browser)                          │
│                   React + TypeScript                         │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Components: Chat, Profile, Sidebar, Auth         │     │
│  │  Services: API Client, Chat, User, Auth           │     │
│  │  State: React Hooks + localStorage                │     │
│  └────────────────┬───────────────────────────────────┘     │
└───────────────────┼──────────────────────────────────────────┘
                    │ HTTP REST + SSE
┌───────────────────▼──────────────────────────────────────────┐
│                Backend (FastAPI)                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Routes: auth, chat, document, report             │     │
│  │           ▼                                        │     │
│  │  Services:                                         │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Agent Service (Agno + Gemini)          │     │     │
│  │  │  • Context-aware prompts                │     │     │
│  │  │  • Streaming responses                  │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  OCR Service (Tesseract)                │     │     │
│  │  │  • PDF/Image text extraction            │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Health Report Agent                     │     │     │
│  │  │  • AI health summary generation          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Context Builder (RAG)                   │     │     │
│  │  │  • ChromaDB vector search                │     │     │
│  │  │  • Semantic document retrieval           │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────┬──────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐      ┌──────▼───────┐
│   MongoDB      │      │  ChromaDB    │
│                │      │              │
│ • users        │      │ • vectors    │
│ • chats        │      │ • embeddings │
│ • documents    │      └──────────────┘
│ • reports      │
│ • sessions     │
│ • files (GridFS)│
└────────────────┘
```

### Request Flow (Chat with RAG)

```
1. User sends message
        ↓
2. Frontend POST /chats/{id}/stream
        ↓
3. Backend authenticates (JWT)
        ↓
4. Context Builder activated
   ├─→ Fetch user health summary
   ├─→ Search ChromaDB for relevant docs
   └─→ Build enhanced prompt
        ↓
5. Agno Agent processes
   ├─→ Gemini AI generates response
   └─→ Stream chunks back
        ↓
6. Frontend receives SSE stream
   └─→ Display real-time response
```

---

## Quick Start

### Prerequisites

✅ **Python 3.9+**
✅ **Node.js 18+**
✅ **MongoDB** (running on port 27017)
✅ **Tesseract OCR** (for document processing)

### 5-Minute Setup

1. **Clone & Navigate:**
   ```bash
   cd health-chatbot
   ```

2. **Configure Environment:**
   
   Create `healthcare-api/.env`:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   MONGODB_URL=mongodb://localhost:27017
   ```

3. **Start Backend:**
   ```bash
   start-backend.bat
   ```
   Server starts at http://localhost:8000

4. **Start Frontend (new terminal):**
   ```bash
   start-frontend.bat
   ```
   App opens at http://localhost:5173

5. **Access Application:**
   - Open http://localhost:5173
   - Sign up for an account
   - Start chatting!

---

## Detailed Setup

### 1. Install Tesseract OCR

**Windows:**
```powershell
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install and add to PATH
```

**macOS:**
```bash
brew install tesseract poppler
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

### 2. Backend Setup

```bash
cd healthcare-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Add GOOGLE_API_KEY and MONGODB_URL

# Start server
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd medicare-chat

# Install dependencies
npm install

# Create .env file (optional)
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

### 4. Verify Installation

- **Backend:** http://localhost:8000/health → `{"status": "healthy"}`
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173

---

## Project Structure

```
health-chatbot/
├── 📂 healthcare-api/                 # Backend (FastAPI)
│   ├── app/
│   │   ├── config/
│   │   │   └── database.py           # MongoDB connection
│   │   ├── models/                   # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── document.py
│   │   ├── routes/                   # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── document.py
│   │   │   └── report.py
│   │   ├── services/                 # Business logic
│   │   │   ├── agent_service.py      # Agno agent
│   │   │   ├── ocr_service.py        # OCR processing
│   │   │   ├── health_report_agent.py
│   │   │   ├── context_builder.py    # RAG system
│   │   │   └── storage_service.py
│   │   ├── utils/
│   │   │   └── tools.py
│   │   ├── dependencies.py
│   │   ├── security.py
│   │   └── main.py                   # FastAPI app
│   ├── data/chromadb/                # Vector store
│   ├── requirements.txt
│   └── .env
│
├── 📂 medicare-chat/                  # Frontend (React)
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── chat/
│   │   │   ├── sidebar/
│   │   │   ├── profile/
│   │   │   ├── auth/
│   │   │   └── ui/                   # Shadcn components
│   │   ├── pages/
│   │   │   ├── Index.tsx
│   │   │   └── NotFound.tsx
│   │   ├── lib/                      # Services
│   │   │   ├── api.ts
│   │   │   ├── chat.ts
│   │   │   ├── user.ts
│   │   │   └── auth.ts
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env
│
├── 📄 BACKEND.md                      # Backend documentation
├── 📄 FRONTEND.md                     # Frontend documentation
├── 📄 README.md                       # GitHub README
├── 📄 start-backend.bat               # Start backend script
└── 📄 start-frontend.bat              # Start frontend script
```

---

## Core Functionality

### 1. Real-time Streaming Chat

**How it works:**

1. User types message
2. Frontend calls `POST /chats/{id}/stream`
3. Backend processes with context from RAG
4. Gemini generates response in chunks
5. Server-Sent Events stream to frontend
6. UI displays text in real-time

**Code Example (Frontend):**
```typescript
await chatService.streamMessage(
  chatId,
  message,
  (chunk) => {
    // Display chunk immediately
    setMessages(prev => [...prev, { content: chunk }]);
  },
  (messageId) => {
    // Complete
    console.log('Message complete:', messageId);
  },
  (error) => {
    // Handle error
    toast({ title: 'Error', description: error });
  }
);
```

---

### 2. OCR Document Processing

**Process:**

1. User uploads PDF/image via Profile → Documents
2. File saved to MongoDB GridFS
3. Background task starts OCR processing
4. Tesseract extracts text
5. Text stored in document model
6. Document added to ChromaDB vector store
7. Status updated: `processed: true`

**Supported Formats:**
- PDF (multi-page)
- JPG, PNG images

---

### 3. Health Summary Generation

**Process:**

1. User clicks "Generate Summary" in Profile
2. Backend fetches:
   - Last 50 chat messages
   - All processed documents (OCR text)
   - Medical reports
3. Health Report Agent analyzes data
4. Gemini generates structured summary
5. Output stored in user profile:
   - Health summary text
   - Medical conditions list
   - Last update timestamp

---

### 4. RAG (Context-Aware Responses)

**How RAG Works:**

```
User Query: "What should I eat for breakfast?"
     ↓
1. Fetch user health summary
   → "Patient has diabetes, age 35"
     ↓
2. Search ChromaDB for relevant docs
   → Top 3 documents about diabetes, diet
     ↓
3. Build enhanced prompt:
   "Patient Health Summary: Has diabetes, age 35
    
    Relevant Medical Records:
    - Document 1: Blood sugar levels elevated...
    - Document 2: Recommended diabetic diet...
    
    Patient Question: What should I eat for breakfast?"
     ↓
4. Send to Gemini AI
     ↓
5. Response: "Given your diabetes, I recommend..."
```

**Benefits:**
- No need to repeat medical history
- Agent aware of past conditions
- Personalized health advice
- Context from uploaded documents

---

## API Reference

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Create account |
| POST | `/login` | User login |
| GET | `/users/me` | Get current user |
| PUT | `/users/me` | Update profile |

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chats/` | Get chat history |
| POST | `/chats/` | Create new chat |
| GET | `/chats/{id}` | Get chat details |
| POST | `/chats/{id}/messages` | Add message (non-streaming) |
| POST | `/chats/{id}/stream` | Add message (streaming) ⭐ |
| DELETE | `/chats/{id}` | Delete chat |

### Document Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/upload` | Upload with OCR ⭐ |
| GET | `/documents/` | List user documents |
| GET | `/documents/{id}` | Get document details |
| GET | `/documents/download/{id}` | Download file |
| DELETE | `/documents/{id}` | Delete document |

### Health Summary Endpoints ⭐ NEW

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/me/health-summary` | Generate AI summary |
| GET | `/users/me/health-summary` | Get current summary |

For detailed API documentation, visit: http://localhost:8000/docs

---

## Development Guide

### Backend Development

**File Organization:**
- **Routes:** Handle HTTP, validate input
- **Services:** Business logic, AI agents
- **Models:** Pydantic schemas
- **Config:** Database connections
- **Utils:** Helper functions

**Adding New Feature:**
1. Create route in `routes/`
2. Create service in `services/`
3. Add models in `models/`
4. Register route in `main.py`

**Running Tests:**
```bash
cd healthcare-api
pytest
```

---

### Frontend Development

**Component Structure:**
- **Pages:** Route components
- **Components:** Reusable UI pieces
- **Lib:** API services
- **Hooks:** Custom React hooks
- **Types:** TypeScript definitions

**Adding New Component:**
```typescript
// src/components/MyComponent.tsx
interface MyComponentProps {
  title: string;
}

export const MyComponent = ({ title }: MyComponentProps) => {
  return <div className="p-4">{title}</div>;
};
```

**Running Tests:**
```bash
cd medicare-chat
npm run test
```

---

## Deployment

### Backend Deployment

**Option 1: Railway/Render**
```bash
# Push to GitHub
# Connect to Railway/Render
# Set environment variables
# Deploy!
```

**Option 2: Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Environment Variables:**
- `GOOGLE_API_KEY` - Gemini API key
- `MONGODB_URL` - MongoDB connection string
- `SECRET_KEY` - JWT secret

---

### Frontend Deployment

**Option 1: Vercel**
```bash
npm install -g vercel
vercel
```

**Option 2: Netlify**
```bash
npm run build
# Upload dist/ folder
```

**Environment Variable:**
- `VITE_API_BASE_URL` - Backend API URL

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Tesseract not found** | Install Tesseract and add to PATH |
| **MongoDB connection error** | Ensure MongoDB is running on port 27017 |
| **CORS error** | Check backend CORS settings include frontend URL |
| **OCR processing stuck** | Check Tesseract installation and poppler (for PDFs) |
| **ChromaDB error** | Delete `data/chromadb/` and restart |
| **JWT token expired** | Login again to get new token |

### Debug Mode

**Backend:**
```bash
# Enable debug logging
uvicorn app.main:app --reload --log-level debug
```

**Frontend:**
```bash
# Check browser console (F12)
# Check Network tab for API calls
```

---

## Performance Tips

- **OCR:** Processing takes 5-30 seconds per document (background task)
- **Health Summary:** Generation takes 10-60 seconds (AI processing)
- **Streaming:** Responses appear in real-time (1-2 seconds latency)
- **Vector Search:** < 1 second query time
- **Caching:** Agent service uses singleton pattern

---

## Security

✅ **JWT Authentication** - Secure token-based auth
✅ **Password Hashing** - bcrypt with salt
✅ **User Isolation** - All data scoped to user_id
✅ **File Validation** - Type and size checks
✅ **CORS Protection** - Restricted origins
✅ **Environment Variables** - Secrets not in code
✅ **Input Validation** - Pydantic models

---

## Contribution Guide

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Run tests: `pytest` and `npm test`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create Pull Request

---

## License

MIT License - See LICENSE file for details

---

## Support & Contact

- **Documentation:** See `BACKEND.md` and `FRONTEND.md`
- **API Docs:** http://localhost:8000/docs
- **Issues:** GitHub Issues
- **Email:** [Your Email]

---

## Acknowledgments

- **Agno** - Agent framework
- **Google Gemini** - AI model
- **Tesseract** - OCR engine
- **ChromaDB** - Vector database
- **FastAPI** - Backend framework
- **React** - Frontend library
- **Shadcn/ui** - UI components

---

## Version History

**v1.0.0** (Current)
- ✅ Real-time streaming chat
- ✅ OCR document processing
- ✅ Health summary generation
- ✅ RAG system implementation
- ✅ Complete UI/UX
- ✅ Production ready

---

## Quick Reference Card

```
📦 Start Backend:    start-backend.bat
📦 Start Frontend:   start-frontend.bat

🌐 Frontend URL:     http://localhost:5173
🔌 Backend URL:      http://localhost:8000
📚 API Docs:         http://localhost:8000/docs

📂 Backend Code:     healthcare-api/app/
📂 Frontend Code:    medicare-chat/src/

📖 Backend Docs:     BACKEND.md
📖 Frontend Docs:    FRONTEND.md
📖 This File:        COPILOT.md
```

---

**Project Status: ✅ Production Ready**

**Last Updated:** January 31, 2026
