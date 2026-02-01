# Backend Documentation - Healthcare AI Chatbot

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Core Services](#core-services)
6. [API Endpoints](#api-endpoints)
7. [Database Models](#database-models)
8. [Setup & Installation](#setup--installation)
9. [Configuration](#configuration)
10. [Development Guide](#development-guide)

---

## Overview

The backend is a **FastAPI-based REST API** with AI-powered health consultation capabilities, featuring:
- 🤖 **Agno Framework** for agent-based AI architecture
- 🔐 **JWT Authentication** with secure password hashing
- 💬 **Real-time Streaming** via Server-Sent Events (SSE)
- 📄 **OCR Processing** with Tesseract for document text extraction
- 🧠 **RAG System** with ChromaDB for context-aware responses
- 🏥 **Health Report Generation** using AI analysis
- 📊 **MongoDB** for data persistence

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client (React)                        │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST + SSE
┌─────────────────────▼───────────────────────────────────┐
│                FastAPI Application                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Routes (Endpoints)                   │  │
│  │  • auth.py      • chat.py     • document.py      │  │
│  │  • report.py                                      │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                   │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │              Services (Business Logic)            │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  agent_service.py                           │ │  │
│  │  │  • Main Agno Agent (Gemini AI)             │ │  │
│  │  │  • Context-aware prompts                    │ │  │
│  │  │  • Session management                       │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  ocr_service.py                             │ │  │
│  │  │  • Tesseract OCR integration                │ │  │
│  │  │  • PDF/Image text extraction                │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  health_report_agent.py                     │ │  │
│  │  │  • AI health summary generation             │ │  │
│  │  │  • Data aggregation from chats/docs         │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  context_builder.py (RAG)                   │ │  │
│  │  │  • ChromaDB vector store                    │ │  │
│  │  │  • Semantic document search                 │ │  │
│  │  │  • Context injection                        │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  storage_service.py                         │ │  │
│  │  │  • GridFS file storage                      │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐          ┌──────▼───────┐
│   MongoDB      │          │  ChromaDB    │
│                │          │              │
│  • users       │          │  • vectors   │
│  • chats       │          │  • embeddings│
│  • documents   │          └──────────────┘
│  • reports     │
│  • sessions    │
└────────────────┘
```

### Request Flow

```
User Request
    ↓
FastAPI Router
    ↓
Authentication Middleware
    ↓
Dependency Injection (get_current_user)
    ↓
Route Handler
    ↓
Service Layer
    ↓ (if chat)
Context Builder (RAG)
    ↓
Agno Agent (Gemini AI)
    ↓
Streaming Response / JSON
    ↓
Client
```

---

## Tech Stack

### Core Framework
- **FastAPI** 0.109.0 - Modern, fast web framework
- **Uvicorn** 0.27.0 - ASGI server
- **Pydantic** 2.5.3 - Data validation

### AI & ML
- **Agno** 0.0.25 - Agent framework
- **Google Gemini** - LLM (gemini-2.0-flash-exp)
- **ChromaDB** 0.4.22 - Vector database for RAG
- **Tesseract OCR** via pytesseract 0.3.10

### Database & Storage
- **MongoDB** via pymongo 4.6.1
- **GridFS** - File storage in MongoDB

### Document Processing
- **Pillow** 10.2.0 - Image processing
- **pdf2image** 1.17.0 - PDF to image conversion
- **pytesseract** 0.3.10 - OCR

### Security
- **python-jose** 3.3.0 - JWT tokens
- **passlib** 1.7.4 - Password hashing
- **bcrypt** 3.2.0 - Secure hashing

### Utilities
- **python-multipart** 0.0.6 - File uploads
- **python-dotenv** 1.0.0 - Environment variables

---

## Project Structure

```
healthcare-api/
├── app/
│   ├── config/
│   │   └── database.py          # MongoDB connection & collections
│   │
│   ├── models/                  # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py              # User, UserCreate, UserResponse
│   │   ├── chat.py              # Chat, Message, ChatCreate
│   │   ├── document.py          # DocumentResponse
│   │   └── report.py            # Report models
│   │
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # /signup, /login, /users/me
│   │   ├── chat.py              # /chats, /chats/{id}/stream
│   │   ├── document.py          # /documents
│   │   └── report.py            # /reports
│   │
│   ├── services/                # Business logic
│   │   ├── agent_service.py     # Main Agno agent
│   │   ├── ocr_service.py       # OCR processing
│   │   ├── health_report_agent.py  # Health summaries
│   │   ├── context_builder.py   # RAG system
│   │   └── storage_service.py   # File storage
│   │
│   ├── utils/
│   │   └── tools.py             # Agent tools
│   │
│   ├── dependencies.py          # get_current_user
│   ├── security.py              # JWT, password hashing
│   └── main.py                  # FastAPI app
│
├── data/
│   └── chromadb/                # Vector store (auto-created)
│
├── uploads/                     # Temporary file storage
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
└── README.md
```

---

## Core Services

### 1. Agent Service (`agent_service.py`)

**Purpose:** Main AI agent using Agno framework

**Key Features:**
- Gemini 2.0 Flash Exp model
- Context-aware prompts via RAG
- Session and memory persistence
- Streaming and non-streaming modes
- Tool integration (DuckDuckGo search)

**Code Structure:**
```python
class HealthcareAgentService:
    _agent = None  # Singleton pattern
    
    @classmethod
    def get_agent(cls):
        # Initialize Agno agent with MongoDB persistence
        
    @classmethod
    def get_response_stream(cls, query, session_id, user_id):
        # Stream response with context
        
    @classmethod
    def get_response(cls, query, session_id, user_id):
        # Non-streaming response with context
```

**Configuration:**
- Model: `gemini-2.0-flash-exp`
- Database: MongoDB for sessions
- History: Last 5 runs in context
- Memory: Auto-updates on run

---

### 2. OCR Service (`ocr_service.py`)

**Purpose:** Extract text from medical documents

**Supported Formats:**
- PDF files (via pdf2image)
- Images (JPG, PNG)

**Code Structure:**
```python
class OCRService:
    @staticmethod
    def extract_text_from_image(image_path: str) -> str
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> Optional[str]
```

**Process:**
1. Save uploaded file to temp location
2. Convert PDF to images (if PDF)
3. Run Tesseract OCR on each page
4. Combine extracted text
5. Clean up temp files

---

### 3. Health Report Agent (`health_report_agent.py`)

**Purpose:** Generate AI-powered health summaries

**Data Sources:**
- Last 50 chat messages
- All processed documents (OCR text)
- Medical reports

**Output:**
- Health summary (3-5 sentences)
- Medical conditions list
- Current symptoms
- Medications
- Key health concerns

**Code Structure:**
```python
class HealthReportAgent:
    @staticmethod
    def get_agent()  # Specialized Gemini agent
    
    @staticmethod
    def fetch_user_chats(user_id, limit=50)
    
    @staticmethod
    def fetch_user_documents(user_id)
    
    @staticmethod
    def generate_health_summary(user_id) -> Dict
```

---

### 4. Context Builder (RAG) (`context_builder.py`)

**Purpose:** Semantic search and context injection

**Key Features:**
- ChromaDB vector store
- Automatic embedding generation
- Semantic document search
- User-scoped queries

**Code Structure:**
```python
class ContextBuilderService:
    _client = None  # ChromaDB client
    _collection = None
    
    @classmethod
    def initialize()  # Setup ChromaDB
    
    @classmethod
    def add_document(document_id, text, metadata)
    
    @classmethod
    def search_relevant_documents(query, user_id, n_results=3)
    
    @classmethod
    def build_context_prompt(user_query, user_id, health_summary)
```

**RAG Process:**
1. User sends query
2. Fetch user's health summary
3. Search ChromaDB for relevant docs (top 3)
4. Build enhanced prompt with context
5. Send to AI agent
6. Return personalized response

---

### 5. Storage Service (`storage_service.py`)

**Purpose:** File storage using MongoDB GridFS

**Key Features:**
- Large file support
- Metadata tracking
- Streaming retrieval

---

## API Endpoints

### Authentication

#### `POST /signup`
Create new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "user_id": "U12345678",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-01-31T10:00:00Z"
}
```

#### `POST /login`
User login (OAuth2 password flow)

**Request:**
```
username: user@example.com
password: password123
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### `GET /users/me`
Get current user profile

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "user_id": "U12345678",
  "email": "user@example.com",
  "full_name": "John Doe",
  "age": 35,
  "gender": "male",
  "health_summary": "Patient has...",
  "medical_conditions": ["Diabetes"],
  "created_at": "2026-01-31T10:00:00Z"
}
```

#### `PUT /users/me`
Update user profile

**Request:**
```json
{
  "full_name": "John Smith",
  "age": 36,
  "gender": "male"
}
```

---

### Health Summary

#### `POST /users/me/health-summary`
Generate AI health summary

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "message": "Health summary generated successfully",
  "health_summary": "Patient is a 35-year-old male with...",
  "medical_conditions": ["Diabetes", "Hypertension"],
  "updated_at": "2026-01-31T10:00:00Z"
}
```

#### `GET /users/me/health-summary`
Get current health summary

**Response:**
```json
{
  "health_summary": "Patient is...",
  "medical_conditions": ["Diabetes"],
  "last_updated": "2026-01-31T10:00:00Z"
}
```

---

### Chat

#### `GET /chats/`
Get all chat history for user

**Response:**
```json
[
  {
    "id": "C12345678",
    "title": "Health Consultation",
    "updated_at": "2026-01-31T10:00:00Z",
    "last_message": "How can I help you today?"
  }
]
```

#### `POST /chats/`
Create new chat

**Request:**
```json
{
  "title": "New Chat",
  "message": "Hello, I need help"
}
```

#### `GET /chats/{chat_id}`
Get specific chat

#### `POST /chats/{chat_id}/messages`
Add message (non-streaming)

**Request:**
```json
{
  "content": "What are symptoms of flu?"
}
```

**Response:**
```json
{
  "id": "M12345678",
  "role": "assistant",
  "content": "Common flu symptoms include...",
  "timestamp": "2026-01-31T10:00:00Z"
}
```

#### `POST /chats/{chat_id}/stream` ⭐ NEW
Add message with streaming response (SSE)

**Request:**
```json
{
  "content": "What are symptoms of flu?"
}
```

**Response:** (Server-Sent Events)
```
data: {"content": "Common", "done": false}

data: {"content": " flu", "done": false}

data: {"content": " symptoms", "done": false}

data: {"content": "", "done": true, "message_id": "M12345678"}
```

#### `DELETE /chats/{chat_id}`
Delete chat

---

### Documents

#### `POST /documents/upload` ⭐ ENHANCED
Upload document with OCR processing

**Request:** (multipart/form-data)
```
file: <file>
description: "Blood test results" (optional)
```

**Response:**
```json
{
  "document_id": "D12345678",
  "user_id": "U12345678",
  "filename": "blood_test.pdf",
  "file_type": "application/pdf",
  "file_size": 125000,
  "description": "Blood test results",
  "extracted_text": null,  // Processing in background
  "processed": false,
  "uploaded_at": "2026-01-31T10:00:00Z"
}
```

**Background Processing:**
1. OCR extracts text
2. Text added to vector store
3. `processed` flag set to `true`

#### `GET /documents/`
Get all user documents

#### `GET /documents/{document_id}`
Get specific document

#### `GET /documents/download/{document_id}`
Download document file

#### `DELETE /documents/{document_id}`
Delete document

---

### Reports

#### `POST /reports/`
Create medical report

#### `GET /reports/`
Get all user reports

#### `GET /reports/{report_id}`
Get specific report

---

## Database Models

### Users Collection

```javascript
{
  _id: ObjectId("..."),
  user_id: "U12345678",              // Unique ID
  email: "user@example.com",         // Unique
  full_name: "John Doe",
  hashed_password: "...",            // bcrypt hash
  created_at: ISODate("2026-01-31"),
  
  // Profile fields
  age: 35,
  gender: "male",
  
  // Health data
  health_summary: "Patient has...",
  medical_conditions: ["Diabetes", "Hypertension"],
  last_summary_update: ISODate("2026-01-31")
}
```

**Indexes:**
- `email` (unique)
- `user_id` (unique)

---

### Chats Collection

```javascript
{
  _id: ObjectId("..."),
  id: "C12345678",                   // Unique chat ID
  user_id: "U12345678",              // Foreign key
  title: "Health Consultation",
  messages: [
    {
      id: "M12345678",
      role: "user",
      content: "Hello",
      timestamp: ISODate("2026-01-31")
    },
    {
      id: "M87654321",
      role: "assistant",
      content: "Hi! How can I help?",
      timestamp: ISODate("2026-01-31")
    }
  ],
  created_at: ISODate("2026-01-31"),
  updated_at: ISODate("2026-01-31")
}
```

**Indexes:**
- `id` (unique)
- `user_id`
- `updated_at`

---

### Documents Collection

```javascript
{
  _id: ObjectId("..."),
  document_id: "D12345678",          // Unique ID
  user_id: "U12345678",              // Foreign key
  file_id: ObjectId("..."),          // GridFS file_id
  filename: "blood_test.pdf",
  file_type: "application/pdf",
  file_size: 125000,
  description: "Blood test results",
  
  // OCR fields
  extracted_text: "Test results show...",
  embedding: [0.1, 0.2, ...],        // Not used (ChromaDB handles)
  processed: true,
  
  uploaded_at: ISODate("2026-01-31")
}
```

**Indexes:**
- `document_id` (unique)
- `user_id`
- `processed`

---

### Agent Sessions Collection (Agno)

```javascript
{
  _id: ObjectId("..."),
  session_id: "C12345678",           // Chat ID
  user_id: "U12345678",
  agent_id: "healthcare-agent",
  runs: [
    {
      query: "What are flu symptoms?",
      response: "Common flu symptoms...",
      timestamp: ISODate("2026-01-31")
    }
  ],
  memory: {
    preferences: {...},
    context: {...}
  },
  created_at: ISODate("2026-01-31"),
  updated_at: ISODate("2026-01-31")
}
```

---

## Setup & Installation

### Prerequisites

1. **Python 3.9+**
2. **MongoDB** (running on localhost:27017)
3. **Tesseract OCR**
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract poppler`
   - Linux: `sudo apt-get install tesseract-ocr poppler-utils`

### Installation Steps

1. **Navigate to backend directory:**
   ```bash
   cd healthcare-api
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   MONGODB_URL=mongodb://localhost:27017
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Access API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## Configuration

### Environment Variables (`.env`)

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Optional (defaults shown)
MONGODB_URL=mongodb://localhost:27017

# JWT Secret (auto-generated if not set)
SECRET_KEY=your_secret_key_here

# Access token expiry (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Tesseract Configuration

If Tesseract not in PATH, set in `ocr_service.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### CORS Configuration

In `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Guide

### Running in Development Mode

```bash
uvicorn app.main:app --reload --port 8000
```

### Running Tests

```bash
pytest
```

### Code Structure Guidelines

1. **Routes:** Handle HTTP requests, validate input, return responses
2. **Services:** Business logic, no HTTP knowledge
3. **Models:** Pydantic models for validation
4. **Dependencies:** Reusable dependencies (auth, database)

### Adding New Endpoint

1. **Create route in `routes/` folder**
2. **Add to `app/main.py`:**
   ```python
   from app.routes import my_route
   app.include_router(my_route.router)
   ```

### Adding New Service

1. **Create service in `services/` folder**
2. **Import in route:**
   ```python
   from app.services.my_service import MyService
   ```

### Database Queries

```python
from app.config.database import get_users_collection

users_collection = get_users_collection()

# Find one
user = users_collection.find_one({"email": "user@example.com"})

# Find many
users = list(users_collection.find({"age": {"$gt": 18}}))

# Insert
users_collection.insert_one({...})

# Update
users_collection.update_one(
    {"user_id": "U12345678"},
    {"$set": {"age": 36}}
)

# Delete
users_collection.delete_one({"user_id": "U12345678"})
```

---

## Performance Optimization

### Background Tasks

OCR processing uses FastAPI BackgroundTasks:
```python
async def process_ocr(document_id, file_path):
    # Heavy OCR processing
    pass

@router.post("/upload")
async def upload(background_tasks: BackgroundTasks, file: UploadFile):
    # Save file immediately
    background_tasks.add_task(process_ocr, doc_id, path)
    return {"status": "processing"}
```

### Caching

Agent service uses singleton pattern:
```python
class HealthcareAgentService:
    _agent = None  # Cached instance
```

### Database Indexing

Ensure indexes on frequently queried fields:
```javascript
db.users.createIndex({ email: 1 }, { unique: true })
db.chats.createIndex({ user_id: 1, updated_at: -1 })
db.documents.createIndex({ user_id: 1, processed: 1 })
```

---

## Security Best Practices

✅ **Authentication:** JWT tokens with expiry
✅ **Password Hashing:** bcrypt with salt
✅ **User Isolation:** All queries filtered by user_id
✅ **File Validation:** Type and size checks
✅ **CORS:** Restricted origins
✅ **Environment Variables:** Secrets in .env
✅ **SQL Injection:** Not applicable (MongoDB)
✅ **Input Validation:** Pydantic models

---

## Deployment

### Production Considerations

1. **Set strong SECRET_KEY**
2. **Use production MongoDB** (Atlas, etc.)
3. **Enable HTTPS**
4. **Configure CORS** for production domain
5. **Set up logging** (file-based)
6. **Monitor API** (health checks)
7. **Scale with Gunicorn:**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Deployment

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Troubleshooting

### Common Issues

**Tesseract not found:**
```bash
# Windows
setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"

# Or in code
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**MongoDB connection error:**
```bash
# Check MongoDB is running
mongod

# Or check connection string
MONGODB_URL=mongodb://localhost:27017
```

**ChromaDB error:**
```bash
# Delete and recreate
rm -rf data/chromadb/
# Restart backend - auto-recreates
```

**CORS error:**
```python
# Check frontend URL in allow_origins
allow_origins=["http://localhost:5173"]
```

---

## API Versioning

Current version: **v1.0.0**

Future versions will use URL prefixing:
```python
app.include_router(auth.router, prefix="/api/v1")
```

---

## License

[Your License Here]

---

## Support

For issues or questions:
1. Check API docs: http://localhost:8000/docs
2. Review logs in console
3. Check MongoDB connection
4. Verify environment variables

---

**Backend Status: ✅ Production Ready**
