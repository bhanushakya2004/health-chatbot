# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│                  (React + TypeScript + Vite)                 │
│                    Port: 5173                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                     App.tsx                            │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │          AuthProvider (useAuth)                 │  │  │
│  │  │    - isAuthenticated                            │  │  │
│  │  │    - login(username, password)                  │  │  │
│  │  │    - signup(email, password, name)              │  │  │
│  │  │    - logout()                                   │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                        │                               │  │
│  │  ┌─────────────────────▼───────────────────────────┐  │  │
│  │  │         ProtectedRoute                           │  │  │
│  │  │  - Checks authentication                         │  │  │
│  │  │  - Shows login if not authenticated              │  │  │
│  │  └─────────────────────┬───────────────────────────┘  │  │
│  │                        │                               │  │
│  │  ┌─────────────────────▼───────────────────────────┐  │  │
│  │  │           Index Page (Main Chat)                 │  │  │
│  │  │  ├─ Sidebar                                      │  │  │
│  │  │  │   ├─ Logo                                     │  │  │
│  │  │  │   ├─ New Chat Button                          │  │  │
│  │  │  │   ├─ Chat History                             │  │  │
│  │  │  │   └─ Login/Logout Buttons                     │  │  │
│  │  │  │                                                │  │  │
│  │  │  ├─ ChatArea                                     │  │  │
│  │  │  │   ├─ ChatHeader                               │  │  │
│  │  │  │   ├─ Messages                                 │  │  │
│  │  │  │   └─ ChatInput                                │  │  │
│  │  │  │                                                │  │  │
│  │  │  └─ Modals                                       │  │  │
│  │  │      ├─ AuthModal (Login/Signup)                 │  │  │
│  │  │      ├─ ProfileModal                             │  │  │
│  │  │      └─ AboutModal                               │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌─────────────────────────▼──────────────────────────┐    │
│  │              API Services Layer                     │    │
│  │                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │   api.ts     │  │   auth.ts    │  │ chat.ts  │ │    │
│  │  │              │  │              │  │          │ │    │
│  │  │ - get()      │  │ - login()    │  │ - send   │ │    │
│  │  │ - post()     │  │ - signup()   │  │   Message│ │    │
│  │  │ - put()      │  │ - logout()   │  │   ()     │ │    │
│  │  │ - delete()   │  │ - getToken() │  │          │ │    │
│  │  │ - postForm   │  │              │  │          │ │    │
│  │  │   Data()     │  │              │  │          │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │    │
│  └──────────────────────────────────────────────────────┘    │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            │ CORS Enabled
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│                   (FastAPI + Python)                         │
│                      Port: 8000                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    FastAPI App                         │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              CORS Middleware                     │  │  │
│  │  │  - Allow Origins: ["*"]                          │  │  │
│  │  │  - Allow Credentials: True                       │  │  │
│  │  │  - Allow Methods: ["*"]                          │  │  │
│  │  │  - Allow Headers: ["*"]                          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │               API Routes                         │  │  │
│  │  │                                                   │  │  │
│  │  │  Authentication Routes (/auth.py)                │  │  │
│  │  │  ┌─────────────────────────────────────────┐    │  │  │
│  │  │  │ POST /signup                             │    │  │  │
│  │  │  │  - Input: email, password, full_name     │    │  │  │
│  │  │  │  - Output: User object                   │    │  │  │
│  │  │  │  - Creates user in MongoDB               │    │  │  │
│  │  │  └─────────────────────────────────────────┘    │  │  │
│  │  │  ┌─────────────────────────────────────────┐    │  │  │
│  │  │  │ POST /login                              │    │  │  │
│  │  │  │  - Input: FormData(username, password)   │    │  │  │
│  │  │  │  - Output: { access_token, token_type }  │    │  │  │
│  │  │  │  - Returns JWT token                     │    │  │  │
│  │  │  └─────────────────────────────────────────┘    │  │  │
│  │  │                                                   │  │  │
│  │  │  Chat Routes (/chat.py)                          │  │  │
│  │  │  ┌─────────────────────────────────────────┐    │  │  │
│  │  │  │ POST /healthchat 🔒                      │    │  │  │
│  │  │  │  - Requires: JWT Token                   │    │  │  │
│  │  │  │  - Input: { message }                    │    │  │  │
│  │  │  │  - Output: { response }                  │    │  │  │
│  │  │  │  - AI-powered health consultation        │    │  │  │
│  │  │  └─────────────────────────────────────────┘    │  │  │
│  │  │                                                   │  │  │
│  │  │  Other Routes (Not Currently Used)               │  │  │
│  │  │  - /patients (CRUD operations)                   │  │  │
│  │  │  - /reports (Medical reports)                    │  │  │
│  │  │  - /documents (File uploads)                     │  │  │
│  │  └───────────────────────────────────────────────────┘  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │            Security Layer                        │  │  │
│  │  │                                                   │  │  │
│  │  │  - JWT Token Generation (python-jose)           │  │  │
│  │  │  - Password Hashing (bcrypt)                     │  │  │
│  │  │  - OAuth2PasswordBearer                          │  │  │
│  │  │  - Token Expiry: 30 minutes                      │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            │ PyMongo
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│                        MongoDB                               │
│                   Port: 27017                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  users          │  │  patients       │  (Not used yet)   │
│  │  ├─ user_id     │  │  ├─ patient_id  │                   │
│  │  ├─ email       │  │  ├─ name        │                   │
│  │  ├─ full_name   │  │  ├─ age         │                   │
│  │  ├─ hashed_pwd  │  │  └─ ...         │                   │
│  │  └─ created_at  │  └─────────────────┘                   │
│  └─────────────────┘                                         │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  reports        │  │  documents      │  (Not used yet)   │
│  │  └─ ...         │  │  └─ ...         │                   │
│  └─────────────────┘  └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Authentication Flow

```
User Action          Frontend                Backend              Database
─────────────────────────────────────────────────────────────────────────
                                                                          
Click "Sign up"  →  AuthModal opens                                      
                                                                          
Fill form &      →  authService.signup()                                 
Submit               ├─ POST /signup      →  Create user     →  Insert   
                     │                        Hash password      user doc 
                     │                        ◄─────────────     ◄─────  
                     │                        Return user                 
                     │                                                    
                     └─ authService.login()                               
                        POST /login        →  Verify password →  Find    
                                              Generate JWT        user    
                        ◄─────────────────    Return token      ◄─────   
                        Store in localStorage                            
                        Update auth state                                 
                                                                          
                     ProtectedRoute allows access                        
```

### 2. Chat Message Flow

```
User Action          Frontend                Backend              AI Service
────────────────────────────────────────────────────────────────────────────
                                                                             
Type message     →  ChatInput component                                     
Press Enter                                                                  
                                                                             
                 →  handleSendMessage()                                      
                    ├─ Add user message to UI                               
                    │                                                        
                    └─ chatService.sendMessage()                            
                       ├─ Add Bearer token                                  
                       │  Authorization: Bearer <JWT>                       
                       │                                                     
                       └─ POST /healthchat  →  Verify JWT token             
                                               Extract user info            
                                               ├─ Process message            
                                               │                             
                                               └─ Call AI (Agno)  →  Generate
                          ◄─────────────────   Return response     ◄───── response
                          { response: "..." }                              
                          │                                                 
                          └─ Add AI message to UI                           
```

### 3. Token Management

```
┌────────────────────────────────────────────────┐
│              Token Lifecycle                    │
└────────────────────────────────────────────────┘

1. Login/Signup
   ↓
2. Server generates JWT
   ↓
3. Token stored in localStorage
   key: "access_token"
   value: "eyJhbGc..."
   ↓
4. Token automatically added to all API requests
   via api.ts → getHeaders()
   ↓
5. Server validates token on protected routes
   ↓
6. Token expires after 30 minutes
   ↓
7. User must login again
```

## Component Hierarchy

```
App
└── AuthProvider
    └── BrowserRouter
        └── Routes
            ├── Route "/"
            │   └── ProtectedRoute
            │       └── Index
            │           ├── Sidebar
            │           │   ├── Logo
            │           │   ├── Button: New Chat
            │           │   ├── ChatHistory[]
            │           │   └── Auth Buttons
            │           │       ├── Login (if not auth)
            │           │       ├── Signup (if not auth)
            │           │       └── Logout (if auth)
            │           │
            │           ├── ChatArea
            │           │   ├── ChatHeader
            │           │   ├── Messages[]
            │           │   │   └── ChatMessage
            │           │   └── ChatInput
            │           │
            │           └── Modals
            │               ├── AuthModal
            │               ├── ProfileModal
            │               └── AboutModal
            │
            └── Route "*"
                └── NotFound
```

## State Management

```
┌─────────────────────────────────────────────┐
│            Authentication State             │
│         (hooks/useAuth.tsx)                 │
├─────────────────────────────────────────────┤
│ - isAuthenticated: boolean                  │
│ - isLoading: boolean                        │
│ - login(username, password): Promise        │
│ - signup(email, password, name): Promise    │
│ - logout(): void                            │
└─────────────────────────────────────────────┘
                    │
                    │ Provides to all components
                    ▼
┌─────────────────────────────────────────────┐
│              Chat State                     │
│         (pages/Index.tsx)                   │
├─────────────────────────────────────────────┤
│ - chats: Chat[]                             │
│ - activeChatId: string | null               │
│ - isTyping: boolean                         │
│ - user: UserProfile                         │
│ - medicalRecords: MedicalRecord[]           │
└─────────────────────────────────────────────┘
```

## Security Flow

```
┌──────────────────────────────────────────────┐
│          Security Measures                    │
└──────────────────────────────────────────────┘

Frontend Security:
├─ Protected Routes (ProtectedRoute.tsx)
│  └─ Checks authentication before rendering
│
├─ Token Storage (localStorage)
│  └─ Automatically attached to requests
│
└─ API Client (lib/api.ts)
   └─ Adds Authorization header
   └─ Handles 401 errors

Backend Security:
├─ CORS Middleware
│  └─ Controls allowed origins
│
├─ Password Hashing (bcrypt)
│  └─ Never stores plain passwords
│
├─ JWT Tokens
│  └─ Signed with SECRET_KEY
│  └─ Expires after 30 minutes
│
└─ OAuth2PasswordBearer
   └─ Validates tokens on protected routes
```

---

**Legend:**
- 🔒 = Protected endpoint (requires authentication)
- → = Data flow direction
- ▼ = Hierarchical relationship
- ├─ = Tree branch
- └─ = Tree end
