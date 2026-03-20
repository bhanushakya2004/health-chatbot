# Healthcare Chatbot — Full Rebuild Plan

---

## Current Project: Honest Assessment

### What Works
- Good idea: RAG + OCR + AI agent for personal healthcare
- FastAPI backend structure is reasonable
- Emergency detection guardrails are thoughtful
- ChromaDB integration exists (though poorly implemented)

### What Doesn't Work / Core Problems

| Area | Problem |
|------|---------|
| **Auth** | DIY JWT, no refresh tokens, no logout/revoke, localStorage (XSS), no MFA, no email verify |
| **Database** | MongoDB with no indexes, unbounded chat arrays, no schema enforcement, sensitive health data unencrypted |
| **RAG** | Word-count chunking (breaks sentences), no chunk overlap, no medical embeddings, no reranking, only 3 results |
| **Agent** | Single-model, no memory beyond 5 turns, regex guardrails (bypassable), hallucinations undetected |
| **Frontend** | Web-only, localStorage tokens, no token refresh, inconsistent API key naming |
| **Docker** | CORS `allow_origins=["*"]` + credentials=True (critical security bug), secrets hardcoded in compose |
| **Code** | print() in production, no tests, singletons, N+1 DB queries, no rate limiting |

---

## New Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              React Native App (iOS + Android)            │
│  • Expo managed workflow                                 │
│  • Secure token storage (expo-secure-store)              │
│  • Chat + Document upload + Health dashboard            │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS + JWT (from Keycloak)
         ┌─────────────▼─────────────┐
         │     Traefik (reverse      │
         │  proxy + TLS termination) │
         └─────────────┬─────────────┘
                       │
       ┌───────────────┼───────────────────┐
       │               │                   │
┌──────▼──────┐  ┌──────▼──────┐  ┌───────▼──────┐
│  Keycloak   │  │  FastAPI    │  │   (future    │
│  (Auth)     │  │  Backend    │  │   services)  │
│  port:8080  │  │  port:8000  │  └──────────────┘
└──────┬──────┘  └──────┬──────┘
       │                │
       │    ┌───────────┼──────────────┐
       │    │           │              │
   ┌───▼────▼──┐  ┌─────▼───┐  ┌──────▼─────┐
   │ PostgreSQL│  │ChromaDB │  │   MinIO    │
   │ (primary  │  │(vectors)│  │(file store)│
   │  DB)      │  │         │  │            │
   └───────────┘  └─────────┘  └────────────┘
```

---

## Tech Stack Decisions

### 1. Authentication: Keycloak

**Why Keycloak over DIY JWT:**
- OIDC/OAuth2 compliant out of the box
- Refresh tokens, token revocation, logout all built in
- MFA/2FA support (TOTP, WebAuthn)
- Social login (Google, Apple) — useful for patients
- User management UI (admin console)
- Session management (active sessions, force logout)
- Self-hosted (HIPAA-friendly, data stays on your server)
- React Native SDK exists (`@react-native-keycloak/keycloak-react-native`)

**Integration pattern:**
- Keycloak issues access token (JWT) + refresh token
- FastAPI validates token against Keycloak's JWKS endpoint (no shared secret)
- App stores tokens in `expo-secure-store` (encrypted, not localStorage)

### 2. Database: PostgreSQL + pgvector (optional) + Alembic

**Why PostgreSQL over MongoDB:**
- Schema enforcement (HIPAA needs auditable, structured data)
- Full ACID transactions (critical for health records)
- Row-level encryption with `pgcrypto`
- Proper indexing (GIN, BRIN, partial indexes)
- `pgvector` extension for storing embeddings alongside data (optional, ChromaDB handles vectors)
- Alembic for database migrations (version-controlled schema)
- Mature backup/restore (pg_dump, WAL archiving)

**ORM:** SQLAlchemy 2.0 (async with `asyncpg`)

### 3. Vector DB: ChromaDB (improved)

**Keep ChromaDB but fix it:**
- Medical-domain embeddings: `BAAI/bge-large-en-v1.5` or `pritamdeka/S-PubMedBert-MS-MARCO`
- Semantic chunking: sentence-boundary aware, 300-token chunks with 50-token overlap
- Hybrid search: BM25 sparse + dense vector (weighted combination)
- Reranking: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Separate collections: `lab_reports`, `prescriptions`, `clinical_notes`, `general_docs`
- Metadata enrichment: document_type, date, importance_score, source

### 4. File Storage: MinIO

**Why MinIO over GridFS:**
- S3-compatible API (easy migration to AWS S3 later)
- Self-hosted, fully private
- Object versioning (keep old document versions)
- Pre-signed URLs for secure direct download
- Bucket policies for access control
- Much better than GridFS for files

### 5. Frontend: React Native (Expo)

**Why Expo over bare React Native:**
- Faster development (no Xcode/Android Studio for most tasks)
- Expo Go for instant testing on physical device
- EAS Build for cloud builds (no local machine requirements)
- `expo-secure-store` for encrypted token storage (vs localStorage)
- `expo-document-picker` for document uploads
- `expo-notifications` for health reminders
- Same TypeScript/React knowledge transfers

**Key libraries:**
- `@tanstack/react-query` — API state management
- `expo-secure-store` — encrypted token storage
- `react-native-reanimated` — smooth animations
- `nativewind` — Tailwind-like styling for RN
- `react-native-gifted-chat` or custom — chat UI

### 6. Agentic System: Multi-Agent with LangGraph

**Why replace Agno with LangGraph:**
- Graph-based agent orchestration (explicit state machine)
- Persistent checkpointing (conversation memory survives restarts)
- Parallel tool execution
- Human-in-the-loop support
- Production-tested at scale
- Works with any LLM (Gemini, OpenAI, local models)

**New agent architecture:**
```
User Message
    │
    ▼
┌─────────────────┐
│  Supervisor     │  ← Routes to appropriate specialist
│  Agent          │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌───────┐  ┌──────────┐  ┌────────────┐
│ RAG   │  │  Medical │  │ Emergency  │
│ Agent │  │  Tools   │  │  Detector  │
│       │  │  Agent   │  │            │
└───────┘  └──────────┘  └────────────┘
    │           │
    ▼           ▼
ChromaDB    PostgreSQL
(vectors)   (patient data)
```

**Agents:**
1. **Supervisor**: Analyzes query, routes to appropriate specialist, merges responses
2. **RAG Agent**: Retrieves relevant documents from ChromaDB, formats context
3. **Medical Tools Agent**: Queries patient data (labs, prescriptions, vitals) from PostgreSQL
4. **Emergency Detector**: Runs in parallel, flags emergencies immediately
5. **Response Validator**: Checks final response for hallucinations, adds citations

### 7. AI Model: Gemini 2.0 Flash + Fallback

**Keep Gemini but add:**
- Structured output (Pydantic schemas for agent tool calls)
- Grounding with Google Search for evidence-based answers
- Model fallback chain: Gemini 2.0 Flash → Gemini 1.5 Pro → local Ollama
- Response confidence scoring

### 8. Infrastructure: Docker Compose (fully self-hosted)

All services containerized, single `docker-compose up` command.

---

## Database Schema (PostgreSQL)

```sql
-- Users (managed by Keycloak, mirrored here for app data)
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keycloak_id UUID UNIQUE NOT NULL,  -- Links to Keycloak user
    email       TEXT UNIQUE NOT NULL,
    full_name   TEXT NOT NULL,
    date_of_birth DATE,
    gender      TEXT CHECK (gender IN ('male', 'female', 'other', 'prefer_not_to_say')),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Health Profile (separate from user auth data)
CREATE TABLE health_profiles (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    blood_type       TEXT,
    allergies        TEXT[],
    chronic_conditions TEXT[],
    current_medications TEXT[],
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    health_summary   TEXT,
    summary_updated_at TIMESTAMPTZ,
    UNIQUE(user_id)
);

-- Documents (metadata only, file in MinIO)
CREATE TABLE documents (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
    filename      TEXT NOT NULL,
    original_name TEXT NOT NULL,
    document_type TEXT CHECK (document_type IN ('lab_report', 'prescription', 'imaging', 'clinical_note', 'other')),
    minio_object  TEXT NOT NULL,  -- MinIO object key
    file_size     BIGINT,
    mime_type     TEXT,
    extracted_text TEXT,          -- OCR output
    ocr_status    TEXT DEFAULT 'pending' CHECK (ocr_status IN ('pending', 'processing', 'done', 'failed')),
    chroma_indexed BOOLEAN DEFAULT FALSE,
    uploaded_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID REFERENCES users(id) ON DELETE CASCADE,
    title      TEXT NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chat Messages (separate table, not embedded array)
CREATE TABLE chat_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role        TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content     TEXT NOT NULL,
    metadata    JSONB DEFAULT '{}',  -- tool calls, citations, confidence
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Health Reports (AI-generated summaries)
CREATE TABLE health_reports (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    content     TEXT NOT NULL,
    model_used  TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Log (HIPAA compliance)
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    user_id     UUID REFERENCES users(id),
    action      TEXT NOT NULL,
    resource    TEXT NOT NULL,
    resource_id UUID,
    ip_address  INET,
    user_agent  TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id, updated_at DESC);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id, created_at);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id, created_at DESC);
```

---

## New Backend Structure

```
healthcare-api/
├── app/
│   ├── main.py                    # FastAPI app, startup
│   ├── config/
│   │   ├── settings.py            # Pydantic Settings (env vars)
│   │   ├── database.py            # SQLAlchemy async engine
│   │   ├── keycloak.py            # Keycloak JWKS validator
│   │   └── minio.py               # MinIO client
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── health_profile.py
│   ├── schemas/                   # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── document.py
│   ├── routes/
│   │   ├── auth.py                # Keycloak token exchange, user sync
│   │   ├── chat.py                # Chat + SSE streaming
│   │   ├── documents.py           # Upload, OCR, indexing
│   │   ├── health.py              # Health profile, reports
│   │   └── admin.py               # Admin endpoints
│   ├── agents/                    # LangGraph agent system
│   │   ├── graph.py               # Agent graph definition
│   │   ├── supervisor.py          # Routing supervisor
│   │   ├── rag_agent.py           # ChromaDB retrieval
│   │   ├── medical_agent.py       # Patient data tools
│   │   ├── emergency_agent.py     # Emergency detection
│   │   ├── validator.py           # Response validation
│   │   └── tools/
│   │       ├── patient_tools.py   # DB query tools
│   │       ├── search_tools.py    # Web search tools
│   │       └── document_tools.py  # Document retrieval
│   ├── services/
│   │   ├── rag_service.py         # ChromaDB operations (improved)
│   │   ├── ocr_service.py         # Tesseract OCR
│   │   ├── storage_service.py     # MinIO operations
│   │   └── report_service.py      # Health report generation
│   ├── middleware/
│   │   ├── auth.py                # Keycloak token validation
│   │   ├── rate_limit.py          # Rate limiting (Redis)
│   │   ├── audit.py               # Audit logging
│   │   └── logging.py             # Request logging
│   └── utils/
│       ├── chunking.py            # Semantic text chunking
│       ├── embeddings.py          # Embedding model wrapper
│       └── prompts.py             # System prompts
├── alembic/                       # Database migrations
│   ├── env.py
│   └── versions/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt
└── Dockerfile
```

---

## New React Native App Structure

```
healthcare-app/
├── app/                           # Expo Router file-based routing
│   ├── _layout.tsx                # Root layout (auth provider)
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx            # Tab navigator
│   │   ├── chat.tsx               # Chat list + new chat
│   │   ├── documents.tsx          # Document management
│   │   ├── health.tsx             # Health dashboard
│   │   └── profile.tsx            # Profile + settings
│   └── chat/
│       └── [id].tsx               # Chat conversation screen
├── components/
│   ├── chat/
│   │   ├── MessageBubble.tsx
│   │   ├── ChatInput.tsx
│   │   ├── StreamingMessage.tsx   # SSE streaming display
│   │   └── EmergencyAlert.tsx
│   ├── documents/
│   │   ├── DocumentCard.tsx
│   │   └── UploadSheet.tsx
│   ├── health/
│   │   ├── HealthSummaryCard.tsx
│   │   └── MetricChart.tsx
│   └── ui/                        # Custom component library
├── lib/
│   ├── api/
│   │   ├── client.ts              # Axios with interceptors
│   │   ├── chat.ts
│   │   ├── documents.ts
│   │   └── health.ts
│   ├── auth/
│   │   ├── keycloak.ts            # Keycloak RN client
│   │   └── tokens.ts              # expo-secure-store wrapper
│   └── query/                     # React Query hooks
│       ├── useChats.ts
│       ├── useDocuments.ts
│       └── useHealth.ts
├── types/
├── constants/
└── package.json
```

---

## Docker Compose (Full Stack)

```yaml
# 10 self-hosted services, single docker-compose up

services:

  # ── Reverse Proxy ──────────────────────────────────────
  traefik:
    image: traefik:v3
    ports: ["80:80", "443:443", "8080:8080"]  # 8080 = traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik/traefik.yml:/traefik.yml
      - ./traefik/certs:/certs
    networks: [healthcare-net]

  # ── Authentication ─────────────────────────────────────
  keycloak-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: ${KEYCLOAK_DB_PASSWORD}
    volumes: [keycloak-db-data:/var/lib/postgresql/data]
    networks: [healthcare-net]

  keycloak:
    image: quay.io/keycloak/keycloak:24
    command: start-dev  # use 'start' in production with TLS
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://keycloak-db/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${KEYCLOAK_DB_PASSWORD}
      KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN_USER}
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
      KC_HOSTNAME: auth.localhost  # or your domain
    depends_on: [keycloak-db]
    ports: ["8080:8080"]
    networks: [healthcare-net]

  # ── Application Database ───────────────────────────────
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: healthcare
      POSTGRES_USER: healthcare
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports: ["5432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U healthcare"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks: [healthcare-net]

  # ── Cache & Rate Limiting ──────────────────────────────
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes: [redis-data:/data]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
    networks: [healthcare-net]

  # ── File Storage ───────────────────────────────────────
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes: [minio-data:/data]
    ports: ["9000:9000", "9001:9001"]  # 9001 = MinIO console
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    networks: [healthcare-net]

  # ── Vector Database ────────────────────────────────────
  chromadb:
    image: chromadb/chroma:latest
    environment:
      IS_PERSISTENT: "TRUE"
      PERSIST_DIRECTORY: /chroma/data
      CHROMA_SERVER_AUTH_CREDENTIALS: ${CHROMA_AUTH_TOKEN}
      CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER: chromadb.auth.token.TokenConfigServerAuthCredentialsProvider
      CHROMA_SERVER_AUTH_PROVIDER: chromadb.auth.token.TokenAuthServerProvider
    volumes: [chroma-data:/chroma/data]
    ports: ["8001:8000"]
    networks: [healthcare-net]

  # ── Backend API ────────────────────────────────────────
  backend:
    build:
      context: ./healthcare-api
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://healthcare:${POSTGRES_PASSWORD}@postgres/healthcare
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      CHROMA_URL: http://chromadb:8000
      CHROMA_AUTH_TOKEN: ${CHROMA_AUTH_TOKEN}
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: ${MINIO_ROOT_USER}
      MINIO_SECRET_KEY: ${MINIO_ROOT_PASSWORD}
      KEYCLOAK_URL: http://keycloak:8080
      KEYCLOAK_REALM: healthcare
      KEYCLOAK_CLIENT_ID: healthcare-api
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
      ENVIRONMENT: production
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_healthy }
      chromadb: { condition: service_started }
      minio: { condition: service_healthy }
      keycloak: { condition: service_started }
    ports: ["8000:8000"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    networks: [healthcare-net]

  # ── Database Migrations ────────────────────────────────
  db-migrate:
    build:
      context: ./healthcare-api
      dockerfile: Dockerfile
    command: alembic upgrade head
    environment:
      DATABASE_URL: postgresql+asyncpg://healthcare:${POSTGRES_PASSWORD}@postgres/healthcare
    depends_on:
      postgres: { condition: service_healthy }
    networks: [healthcare-net]
    restart: "no"

  # ── Monitoring (optional but recommended) ─────────────
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
    volumes: [pgadmin-data:/var/lib/pgadmin]
    ports: ["5050:80"]
    depends_on: [postgres]
    networks: [healthcare-net]

networks:
  healthcare-net:
    driver: bridge

volumes:
  keycloak-db-data:
  postgres-data:
  redis-data:
  minio-data:
  chroma-data:
  pgadmin-data:
```

---

## Phased Implementation Plan

### Phase 1: Infrastructure & Database (Week 1–2)
Foundation first. Everything depends on this.

**Tasks:**
- [ ] Set up PostgreSQL with full schema + Alembic migrations
- [ ] Set up MinIO (replace GridFS)
- [ ] Set up Redis (rate limiting + session cache)
- [ ] Set up ChromaDB in server mode (not embedded file)
- [ ] Set up Traefik reverse proxy
- [ ] Create `.env` template with all required variables
- [ ] Run `docker-compose up` with all infrastructure services

**Deliverable:** All infrastructure running, verified with health checks

---

### Phase 2: Keycloak Authentication (Week 2–3)
Replace all DIY JWT code with Keycloak.

**Tasks:**
- [ ] Deploy Keycloak, create `healthcare` realm
- [ ] Create clients: `healthcare-api` (confidential), `healthcare-app` (public/PKCE)
- [ ] Configure Keycloak realm settings: password policies, session lengths, token expiry
- [ ] FastAPI: Replace `security.py` with Keycloak JWKS token validator
- [ ] FastAPI: Replace `dependencies.py` `get_current_user` to sync Keycloak user → PostgreSQL
- [ ] FastAPI: Replace `/auth/signup` + `/auth/login` with Keycloak registration/login redirect
- [ ] Add Keycloak admin API calls for user management (from backend)
- [ ] Test token flow: login → access token → API call → refresh → logout

**Key code change:**
```python
# Old: validate against shared SECRET_KEY
# New: validate against Keycloak JWKS (public key, no shared secret)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = await keycloak_client.decode_token(token)
    keycloak_id = payload["sub"]
    user = await db.users.get_by_keycloak_id(keycloak_id)
    if not user:
        user = await db.users.create_from_keycloak(payload)
    return user
```

**Deliverable:** Auth fully through Keycloak, all DIY JWT code removed

---

### Phase 3: Backend Rewrite (Week 3–5)
Migrate from MongoDB to PostgreSQL, improve all services.

**Tasks:**
- [ ] SQLAlchemy 2.0 async models for all tables
- [ ] Alembic migration scripts
- [ ] Migrate user service (CRUD via SQLAlchemy)
- [ ] Migrate chat service (sessions + paginated messages, no arrays)
- [ ] Migrate document service (metadata in PG, files in MinIO)
- [ ] Improve OCR pipeline (better extraction, status tracking)
- [ ] Fix ChromaDB service: semantic chunking, medical embeddings, metadata
- [ ] Add rate limiting middleware (slowapi + Redis)
- [ ] Add audit logging middleware
- [ ] Fix CORS (specific origins only)
- [ ] Proper structured logging (structlog)
- [ ] Pydantic Settings for all config (no hardcoded defaults)

**Deliverable:** Backend working with PostgreSQL + MinIO + ChromaDB server mode

---

### Phase 4: Agentic System Rebuild (Week 5–7)
The most complex part. New multi-agent LangGraph system.

**Tasks:**
- [ ] Install and configure LangGraph
- [ ] Build agent state schema (TypedDict with conversation state)
- [ ] Build Emergency Detector node (runs first, parallel, fast)
- [ ] Build RAG Agent node (ChromaDB retrieval + reranking)
- [ ] Build Medical Tools Agent (patient data from PostgreSQL)
- [ ] Build Supervisor node (route queries to appropriate agents)
- [ ] Build Response Validator node (hallucination check, citations)
- [ ] Configure LangGraph checkpointing (PostgreSQL-backed persistence)
- [ ] Implement streaming through LangGraph
- [ ] Improve system prompts (chain-of-thought, medical reasoning steps)
- [ ] Add confidence scoring to responses
- [ ] Test with real healthcare scenarios

**Agent graph:**
```python
graph = StateGraph(HealthcareState)
graph.add_node("emergency_check", emergency_detector)
graph.add_node("supervisor", supervisor_agent)
graph.add_node("rag_agent", rag_agent)
graph.add_node("medical_tools", medical_tools_agent)
graph.add_node("validator", response_validator)

graph.set_entry_point("emergency_check")
graph.add_conditional_edges("emergency_check", route_emergency)
graph.add_conditional_edges("supervisor", route_to_specialist)
graph.add_edge("rag_agent", "validator")
graph.add_edge("medical_tools", "validator")
graph.add_edge("validator", END)
```

**Deliverable:** Multi-agent system with better accuracy, memory, and citations

---

### Phase 5: React Native App (Week 7–10)
Build the mobile app from scratch with Expo.

**Tasks:**
- [ ] Init Expo project with TypeScript + Expo Router
- [ ] Set up NativeWind (Tailwind styling)
- [ ] Set up React Query + Axios API client
- [ ] Keycloak auth integration (`expo-auth-session` + PKCE flow)
- [ ] `expo-secure-store` for token storage
- [ ] Chat list screen + new chat
- [ ] Chat conversation screen with SSE streaming
- [ ] Document upload screen (camera + file picker)
- [ ] Health dashboard screen (profile, conditions, summary)
- [ ] Document viewer
- [ ] Emergency alert component (prominent, 911 prompt)
- [ ] Push notifications (Expo Notifications) for health reminders
- [ ] Offline detection + graceful error handling

**Deliverable:** Working React Native app on iOS + Android

---

### Phase 6: Integration & Hardening (Week 10–11)
Connect everything, secure it.

**Tasks:**
- [ ] Full end-to-end test: signup → chat → upload document → RAG-enhanced response
- [ ] Configure Traefik with TLS (Let's Encrypt or self-signed for dev)
- [ ] Lock down Docker network (services only talk through defined networks)
- [ ] Resource limits on all containers (CPU/memory)
- [ ] Set up log rotation
- [ ] Set up PGAdmin for database access
- [ ] Create backup scripts (PostgreSQL dump + MinIO sync)
- [ ] Performance test: concurrent users, stream latency
- [ ] Security: OWASP top 10 review

**Deliverable:** Production-ready stack running on single machine via `docker-compose up`

---

## Environment Variables (.env template)

```env
# ── PostgreSQL ─────────────────────────────
POSTGRES_PASSWORD=change_this_strong_password

# ── Redis ──────────────────────────────────
REDIS_PASSWORD=change_this_redis_password

# ── Keycloak ───────────────────────────────
KEYCLOAK_ADMIN_USER=admin
KEYCLOAK_ADMIN_PASSWORD=change_this_admin_password
KEYCLOAK_DB_PASSWORD=change_this_keycloak_db_password

# ── MinIO ──────────────────────────────────
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=change_this_minio_password

# ── ChromaDB ───────────────────────────────
CHROMA_AUTH_TOKEN=change_this_chroma_token

# ── AI Models ──────────────────────────────
GOOGLE_API_KEY=your_gemini_api_key_here

# ── PGAdmin (optional) ─────────────────────
PGADMIN_EMAIL=admin@healthcare.local
PGADMIN_PASSWORD=change_this_pgadmin_password

# ── App ────────────────────────────────────
ENVIRONMENT=development
```

Single `.env` file at root → all services read from it.

---

## Services Summary (Self-Hosted, All via Docker)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| Traefik | `traefik:v3` | 80, 443 | Reverse proxy, TLS |
| Keycloak | `keycloak:24` | 8080 | Auth, SSO, MFA |
| Keycloak DB | `postgres:16` | — | Keycloak's DB |
| PostgreSQL | `postgres:16` | 5432 | App database |
| Redis | `redis:7` | 6379 | Cache, rate limits |
| MinIO | `minio/minio` | 9000 | File storage |
| ChromaDB | `chromadb/chroma` | 8001 | Vector embeddings |
| Backend | Custom | 8000 | FastAPI app |
| PGAdmin | `pgadmin4` | 5050 | DB management UI |
| db-migrate | Custom | — | Run migrations (one-shot) |

**Total: 10 services, 1 command.**

---

## What Stays, What Changes, What's New

| Component | Decision | Reason |
|-----------|----------|--------|
| FastAPI | **Keep** (rewrite internals) | Good choice for async Python |
| MongoDB | **Replace** → PostgreSQL | Schema, transactions, HIPAA |
| React | **Replace** → React Native | Mobile-first healthcare |
| DIY JWT | **Replace** → Keycloak | Full auth system, not homemade |
| Agno | **Replace** → LangGraph | Better graph control, memory |
| ChromaDB | **Keep** (fix implementation) | Already there, fix the usage |
| Tesseract OCR | **Keep** | Self-hosted, good enough |
| Gemini | **Keep** (add fallback) | Capable model, cheap |
| GridFS | **Replace** → MinIO | S3-compatible, much better |
| Docker Compose | **Keep** (expand) | Correct tool for self-hosted |
| Agno Tools | **Replace** → LangGraph Tools | Part of agent rewrite |

---

## Immediate Next Steps

1. **Start with Phase 1** — get infrastructure up first
2. **Test credentials:** `testuser@example.com` / `testpass123` still works during migration
3. **Don't migrate data** — the MongoDB data is test data, start fresh with seeded PostgreSQL
4. **Keycloak realm config** — export as JSON after setup so it can be version-controlled

The rebuild touches every layer of the stack. Work phase by phase, don't try to do everything at once. Each phase produces a working deliverable.
