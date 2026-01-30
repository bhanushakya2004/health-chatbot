# Frontend-Backend Integration Guide

## Overview
This document describes the integration between the React frontend (medicare-chat) and FastAPI backend (healthcare-api).

## Setup Instructions

### Backend Setup
1. Navigate to the healthcare-api directory:
   ```bash
   cd healthcare-api
   ```

2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   The backend will run on: http://localhost:8000

### Frontend Setup
1. Navigate to the medicare-chat directory:
   ```bash
   cd medicare-chat
   ```

2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```

3. Create a `.env` file (if not exists):
   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

   The frontend will run on: http://localhost:5173

## API Integration

### Authentication Flow
- **Login**: POST `/login` - Uses OAuth2PasswordRequestForm (form data with username/password)
- **Signup**: POST `/signup` - JSON with email, password, full_name
- **Token Storage**: JWT tokens are stored in localStorage
- **Token Expiry**: Access tokens expire in 30 minutes
- **Protected Routes**: All routes require authentication via ProtectedRoute component

### Chat Integration
- **Endpoint**: POST `/healthchat`
- **Authentication**: Requires Bearer token in Authorization header
- **Request Format**: `{ "message": "your health question" }`
- **Response Format**: `{ "response": "AI response" }`

### CORS Configuration
The backend is configured to accept requests from all origins:
```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

## Architecture

### Frontend Services
- **`lib/api.ts`**: Base API client with authentication headers
- **`lib/auth.ts`**: Authentication service (login, signup, logout, token management)
- **`lib/chat.ts`**: Chat service for health consultation

### Authentication Context
- **`hooks/useAuth.tsx`**: React context provider for global auth state
- **`AuthProvider`**: Wraps the entire app to provide auth state
- **`useAuth`**: Custom hook to access auth functions (login, signup, logout)

### Protected Routes
- **`components/ProtectedRoute.tsx`**: Wraps routes that require authentication
- Shows login modal if user is not authenticated
- Displays loading spinner during auth check

### Components Updated
- **`AuthModal`**: Now calls real authentication APIs
- **`Sidebar`**: Shows logout button when authenticated
- **`Index.tsx`**: Chat messages now use real AI API

## Testing

### Test Authentication
1. Click "Sign up" in the sidebar
2. Enter email, password, and name
3. Submit the form
4. Check if you're logged in (logout button appears)

### Test Chat
1. After logging in, create a new chat
2. Type a health question
3. Press Enter or click Send
4. Verify AI response appears

### Test Logout
1. Click "Log out" in the sidebar
2. Verify you're redirected to login screen
3. Verify token is removed from localStorage

## Troubleshooting

### Backend Not Starting
- Ensure Python dependencies are installed
- Check if MongoDB is running (if required)
- Verify port 8000 is not in use

### Frontend Can't Connect
- Verify backend is running on port 8000
- Check `.env` file has correct VITE_API_BASE_URL
- Check browser console for CORS errors

### Authentication Errors
- Verify backend /login endpoint expects form data (not JSON)
- Check if token is being stored in localStorage
- Verify Authorization header format: `Bearer <token>`

## Next Steps
1. Implement chat history persistence (save to backend)
2. Add user profile management
3. Implement file upload for medical records
4. Add refresh token mechanism
5. Implement proper error boundaries
