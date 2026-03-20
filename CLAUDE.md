# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack healthcare AI chatbot with:
- **Frontend**: React + TypeScript + Vite + Shadcn/ui (`medicare-chat/`)
- **Backend**: FastAPI + Python + MongoDB + ChromaDB (`healthcare-api/`)
- **AI**: Google Gemini 2.0 Flash via Agno framework, with ChromaDB RAG

## Common Commands

### Backend (healthcare-api/)
```bash
# Activate venv first
source .venv/Scripts/activate  # Windows (bash)

# Start dev server
uvicorn app.main:app --reload

# Seed database (first-time setup)
python seed_database.py        # Basic seed
python seed_enhanced.py        # Rich test data (preferred)
```

### Frontend (medicare-chat/)
```bash
npm run dev          # Dev server on port 5173 (not 8080 despite vite config)
npm run build        # Production build
npm run lint         # ESLint
npm test             # Vitest (run once)
npm run test:watch   # Vitest watch mode
```

### Docker (full stack)
```bash
cp .env.template .env   # then add API keys
docker-compose up -d
docker-compose logs -f
```

## Environment Setup

Backend `.env` (in `healthcare-api/.env`):
- `GOOGLE_API_KEY` — required for Gemini AI
- `MONGODB_URL` — defaults to `mongodb://localhost:27017`
- `DATABASE_NAME` — defaults to `healthcare_db`
- `SECRET_KEY` — JWT signing key

Frontend `.env` (in `medicare-chat/.env`):
- `VITE_API_BASE_URL=http://localhost:8000`

See `.env.template` at the root for all variables.

## Architecture

### Request Flow
```
Browser (React) → REST/SSE → FastAPI Routes → Services → AI/DB → Response
```

### Backend Service Layer (`healthcare-api/app/services/`)
| File | Responsibility |
|------|----------------|
| `agent_service.py` | Agno AI agent orchestration using Gemini |
| `context_builder.py` | RAG: ChromaDB vector search for relevant patient context |
| `health_report_agent.py` | AI-generated health summary reports |
| `ocr_service.py` | Tesseract OCR for uploaded medical documents |
| `storage_service.py` | MongoDB GridFS for file storage |
| `guardrails.py` | Safety checks, prompt injection detection, system prompts |
| `prompts.py` | Production AI prompt templates |

### Backend Routes (`healthcare-api/app/routes/`)
- `POST /auth/signup`, `POST /auth/login`, `GET /auth/me`
- `GET/POST /chats`, `GET /chats/{id}` — chat history; SSE streaming on chat
- `POST /documents`, `GET /documents` — upload + OCR pipeline
- `GET/POST /reports` — AI health summaries

### Frontend Key Files (`medicare-chat/src/`)
- `lib/api.ts` — base API client with JWT auth headers
- `lib/chat.ts`, `lib/user.ts`, `lib/auth.ts` — service modules
- `hooks/useAuth.tsx` — auth context/provider
- `components/auth/AuthModal.tsx` — login/signup
- `components/chat/` — ChatArea, ChatInput, ChatMessage (SSE streaming)
- `components/profile/ProfileModal.tsx` — document upload + health summary

### Data Flow for Chat
1. User sends message → `ChatInput.tsx`
2. `lib/chat.ts` opens SSE stream to `POST /chats/{id}/messages`
3. Backend: `agent_service.py` builds context via `context_builder.py` (RAG from ChromaDB)
4. Gemini streams response tokens back via SSE
5. `ChatArea.tsx` renders streamed tokens in real time

### Data Flow for Document Upload
1. User uploads file → `ProfileModal.tsx`
2. `POST /documents` → `storage_service.py` (GridFS) + `ocr_service.py` (Tesseract)
3. Extracted text embedded into ChromaDB vectors (used by RAG in chat)

## Key Conventions

- Path alias `@/` maps to `medicare-chat/src/`
- Backend uses Pydantic v2 models (in `app/models/`)
- All auth is JWT bearer tokens stored in `localStorage`
- FastAPI dependency injection pattern: see `app/dependencies.py` for `get_current_user`
- CORS is open (`allow_origins=["*"]`) in development

## URLs
- Frontend dev: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- MongoDB: mongodb://localhost:27017
