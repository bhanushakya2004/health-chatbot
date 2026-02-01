# Frontend Documentation - Healthcare AI Chatbot

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [Routing](#routing)
9. [Setup & Installation](#setup--installation)
10. [Development Guide](#development-guide)

---

## Overview

The frontend is a **React + TypeScript** single-page application (SPA) featuring:
- 💬 **Real-time Chat Interface** with streaming responses
- 🎨 **Modern UI** built with Shadcn/ui components
- 🔐 **JWT Authentication** with protected routes
- 📱 **Responsive Design** for mobile and desktop
- 🌓 **Dark/Light Mode** support
- 📄 **Document Management** with upload and OCR status
- 🏥 **Health Profile** with AI-generated summaries
- ⚡ **Fast Performance** with Vite build tool

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Application                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │              Pages (Route Components)           │    │
│  │  • Index.tsx (Main chat interface)             │    │
│  │  • NotFound.tsx                                │    │
│  └────────────────┬───────────────────────────────┘    │
│                   │                                     │
│  ┌────────────────▼───────────────────────────────┐    │
│  │              Components                         │    │
│  │  ┌──────────────────────────────────────────┐ │    │
│  │  │  Chat Components                          │ │    │
│  │  │  • ChatArea - Message display             │ │    │
│  │  │  • ChatInput - User input                │ │    │
│  │  │  • ChatHeader - Top bar                  │ │    │
│  │  │  • Message - Individual message          │ │    │
│  │  └──────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────┐ │    │
│  │  │  Sidebar Components                       │ │    │
│  │  │  • Sidebar - Navigation & chat history   │ │    │
│  │  │  • ChatHistoryItem - Chat preview        │ │    │
│  │  └──────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────┐ │    │
│  │  │  Profile Components                       │ │    │
│  │  │  • ProfileModal - User profile editor    │ │    │
│  │  │    - Profile tab                         │ │    │
│  │  │    - Documents tab                       │ │    │
│  │  │    - Health Summary tab                  │ │    │
│  │  └──────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────┐ │    │
│  │  │  Auth Components                          │ │    │
│  │  │  • AuthModal - Login/Signup              │ │    │
│  │  └──────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────┐ │    │
│  │  │  UI Components (Shadcn/ui)               │ │    │
│  │  │  • Button, Input, Dialog, Tabs, etc.    │ │    │
│  │  └──────────────────────────────────────────┘ │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌────────────────────────────────────────────────┐   │
│  │              Services (API Layer)              │   │
│  │  • api.ts - Base API client                   │   │
│  │  • chat.ts - Chat operations                  │   │
│  │  • user.ts - User/document operations         │   │
│  │  • auth.ts - Authentication                   │   │
│  └────────────────┬───────────────────────────────┘   │
│                   │                                    │
│  ┌────────────────▼───────────────────────────────┐   │
│  │              Hooks                              │   │
│  │  • useAuth - Authentication state              │   │
│  │  • use-toast - Toast notifications             │   │
│  └─────────────────────────────────────────────────┘   │
│                                                        │
└────────────────────┬───────────────────────────────────┘
                     │ HTTP/REST + SSE
┌────────────────────▼───────────────────────────────────┐
│                   Backend API                          │
│              (FastAPI on port 8000)                    │
└────────────────────────────────────────────────────────┘
```

### Component Hierarchy

```
App.tsx
  └── BrowserRouter
      └── Routes
          ├── Index.tsx (Main Page)
          │   ├── Sidebar
          │   │   └── ChatHistoryItem (multiple)
          │   ├── ChatHeader
          │   ├── ChatArea
          │   │   └── Message (multiple)
          │   ├── ChatInput
          │   ├── ProfileModal
          │   │   ├── Profile Tab
          │   │   ├── Documents Tab
          │   │   └── Health Summary Tab
          │   ├── AuthModal
          │   └── AboutModal
          └── NotFound.tsx
```

---

## Tech Stack

### Core Framework
- **React** 18.3.1 - UI library
- **TypeScript** 5.6.2 - Type safety
- **Vite** 6.0.1 - Build tool (fast HMR)

### UI & Styling
- **Shadcn/ui** - Component library
- **Radix UI** - Headless components
- **Tailwind CSS** 3.4.1 - Utility-first CSS
- **Lucide React** - Icon library

### Routing & State
- **React Router DOM** 7.1.1 - Client-side routing
- **React Hooks** - State management (useState, useEffect, useCallback)

### Forms & Validation
- **React Hook Form** - Form handling
- **Zod** - Schema validation

### Date Handling
- **date-fns** 4.1.0 - Date formatting

### Development Tools
- **ESLint** - Linting
- **TypeScript** - Type checking
- **Vitest** - Testing (configured)

---

## Project Structure

```
medicare-chat/
├── public/
│   └── vite.svg                # Favicon
│
├── src/
│   ├── components/             # React components
│   │   ├── chat/              # Chat-related components
│   │   │   ├── ChatArea.tsx   # Message display area
│   │   │   ├── ChatHeader.tsx # Top bar with actions
│   │   │   ├── ChatInput.tsx  # User input box
│   │   │   └── Message.tsx    # Individual message
│   │   │
│   │   ├── sidebar/           # Sidebar components
│   │   │   ├── Sidebar.tsx    # Main sidebar
│   │   │   └── ChatHistoryItem.tsx  # Chat list item
│   │   │
│   │   ├── profile/           # Profile components
│   │   │   └── ProfileModal.tsx  # Profile editor
│   │   │
│   │   ├── auth/              # Authentication
│   │   │   └── AuthModal.tsx  # Login/Signup modal
│   │   │
│   │   ├── ui/                # Shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── tabs.tsx
│   │   │   └── ... (30+ components)
│   │   │
│   │   ├── AboutModal.tsx     # About dialog
│   │   └── EmptyState.tsx     # Empty chat state
│   │
│   ├── pages/                 # Route components
│   │   ├── Index.tsx          # Main chat page
│   │   └── NotFound.tsx       # 404 page
│   │
│   ├── lib/                   # Services & utilities
│   │   ├── api.ts             # Base API client
│   │   ├── chat.ts            # Chat service
│   │   ├── user.ts            # User service
│   │   ├── auth.ts            # Auth service
│   │   └── utils.ts           # Helper functions
│   │
│   ├── hooks/                 # Custom hooks
│   │   ├── useAuth.tsx        # Authentication hook
│   │   └── use-toast.ts       # Toast notification hook
│   │
│   ├── types/                 # TypeScript types
│   │   └── chat.ts            # Chat-related types
│   │
│   ├── App.tsx                # Root component
│   ├── main.tsx               # Entry point
│   ├── index.css              # Global styles
│   └── App.css                # App styles
│
├── .env                       # Environment variables
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── vite.config.ts             # Vite config
├── tailwind.config.ts         # Tailwind config
├── components.json            # Shadcn config
└── README.md
```

---

## Core Components

### 1. Index.tsx (Main Page)

**Purpose:** Main chat interface orchestrating all components

**State Management:**
```typescript
// Sidebar state
const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

// Chat state
const [chats, setChats] = useState<ChatHistoryResponse[]>([]);
const [activeChat, setActiveChat] = useState<Chat | null>(null);
const [isTyping, setIsTyping] = useState(false);

// User state
const [user, setUser] = useState<UserProfile | null>(null);

// Modal state
const [profileOpen, setProfileOpen] = useState(false);
const [aboutOpen, setAboutOpen] = useState(false);
const [authOpen, setAuthOpen] = useState(false);
```

**Key Functions:**
- `loadChatHistory()` - Fetch chat list
- `handleNewChat()` - Create new chat
- `handleSelectChat()` - Switch active chat
- `handleSendMessage()` - Send message with streaming
- `handleDeleteChat()` - Delete chat

---

### 2. ChatArea.tsx

**Purpose:** Display chat messages with scroll management

**Features:**
- Auto-scroll to bottom on new messages
- Markdown rendering
- Message grouping by role
- Loading states
- Empty state

**Props:**
```typescript
interface ChatAreaProps {
  messages: Message[];
  isTyping: boolean;
}
```

---

### 3. ChatInput.tsx

**Purpose:** User input with file attachment support

**Features:**
- Text input with auto-resize
- File attachment (drag & drop)
- Send on Enter (Shift+Enter for new line)
- Character count
- Disabled state during typing

**Props:**
```typescript
interface ChatInputProps {
  onSendMessage: (message: string, attachments?: Attachment[]) => void;
  disabled?: boolean;
}
```

---

### 4. ProfileModal.tsx ⭐ NEW

**Purpose:** User profile management with 3 tabs

**Tabs:**
1. **Profile Tab**
   - Name, email, age, gender
   - Save profile button

2. **Documents Tab**
   - Upload medical documents
   - List uploaded documents
   - Processing status indicator
   - Delete documents

3. **Health Summary Tab**
   - Generate AI summary button
   - Display health summary
   - Medical conditions list
   - Last updated timestamp

**Key Features:**
```typescript
// Load user data from backend
const loadUserData = async () => {
  const [userProfile, userDocs] = await Promise.all([
    userService.getCurrentUser(),
    userService.getDocuments()
  ]);
  setUser(userProfile);
  setDocuments(userDocs);
};

// Upload document with OCR
const handleFileUpload = async () => {
  const newDoc = await userService.uploadDocument(file, description);
  setDocuments([newDoc, ...documents]);
};

// Generate health summary
const handleGenerateHealthSummary = async () => {
  const summary = await userService.generateHealthSummary();
  setUser({...user, health_summary: summary.health_summary});
};
```

---

### 5. Sidebar.tsx

**Purpose:** Navigation and chat history

**Features:**
- New chat button
- Chat list with search
- Recent chats
- User profile button
- About button
- Collapse/expand
- Mobile responsive

---

### 6. AuthModal.tsx

**Purpose:** Authentication (login/signup)

**Features:**
- Toggle between login and signup
- Form validation
- Error handling
- JWT token storage

---

## State Management

### Authentication State (`useAuth` hook)

```typescript
const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const login = (token: string) => {
    localStorage.setItem('access_token', token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
  };

  return { isAuthenticated, loading, login, logout };
};
```

### Local State (React Hooks)

Components use `useState`, `useEffect`, and `useCallback` for local state:

```typescript
// State
const [messages, setMessages] = useState<Message[]>([]);

// Side effects
useEffect(() => {
  loadChatHistory();
}, [isAuthenticated]);

// Memoized callbacks
const handleSendMessage = useCallback(async (content: string) => {
  // ... implementation
}, [activeChat, isAuthenticated]);
```

---

## API Integration

### Base API Client (`api.ts`)

```typescript
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse<T>(response);
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> { ... }
  async put<T>(endpoint: string, data: unknown): Promise<T> { ... }
  async delete<T>(endpoint: string): Promise<T> { ... }
  async postFormData<T>(endpoint: string, formData: FormData): Promise<T> { ... }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

---

### Chat Service (`chat.ts`)

```typescript
export const chatService = {
  // Get chat history
  async getChatHistory(): Promise<ChatHistoryResponse[]> {
    return apiClient.get<ChatHistoryResponse[]>('/chats/');
  },

  // Create new chat
  async createChat(title: string, message: string): Promise<Chat> {
    return apiClient.post<Chat>('/chats/', { title, message });
  },

  // Add message (non-streaming)
  async addMessageToChat(chatId: string, message: string): Promise<Message> {
    return apiClient.post<Message>(`/chats/${chatId}/messages`, { content: message });
  },

  // Stream message (SSE) ⭐ NEW
  async streamMessage(
    chatId: string,
    message: string,
    onChunk: (chunk: string) => void,
    onComplete: (messageId: string) => void,
    onError: (error: string) => void
  ): Promise<void> {
    const token = localStorage.getItem('access_token');
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ content: message }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          
          if (data.error) {
            onError(data.error);
            return;
          }
          
          if (data.done) {
            onComplete(data.message_id);
            return;
          }
          
          if (data.content) {
            onChunk(data.content);
          }
        }
      }
    }
  },

  // Delete chat
  async deleteChat(chatId: string): Promise<void> {
    return apiClient.delete<void>(`/chats/${chatId}`);
  },
};
```

---

### User Service (`user.ts`) ⭐ ENHANCED

```typescript
export const userService = {
  // Get current user
  async getCurrentUser(): Promise<UserProfile | null> {
    return apiClient.get<UserProfile>('/users/me');
  },

  // Update user profile
  async updateCurrentUser(data: UserUpdate): Promise<UserProfile> {
    return apiClient.put<UserProfile>('/users/me', data);
  },

  // Generate health summary ⭐ NEW
  async generateHealthSummary(): Promise<HealthSummary> {
    return apiClient.post<HealthSummary>('/users/me/health-summary', {});
  },

  // Get health summary ⭐ NEW
  async getHealthSummary(): Promise<HealthSummary> {
    return apiClient.get<HealthSummary>('/users/me/health-summary');
  },

  // Get user documents ⭐ NEW
  async getDocuments(): Promise<Document[]> {
    return apiClient.get<Document[]>('/documents/');
  },

  // Upload document ⭐ NEW
  async uploadDocument(file: File, description?: string): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    if (description) {
      formData.append('description', description);
    }
    return apiClient.postFormData<Document>('/documents/upload', formData);
  },

  // Delete document ⭐ NEW
  async deleteDocument(documentId: string): Promise<void> {
    return apiClient.delete<void>(`/documents/${documentId}`);
  },
};
```

---

## Routing

### Route Configuration (`App.tsx`)

```typescript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Index from './pages/Index';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}
```

### Protected Routes

Authentication handled in components:
```typescript
const { isAuthenticated } = useAuth();

useEffect(() => {
  if (!isAuthenticated) {
    setAuthOpen(true);  // Show login modal
  }
}, [isAuthenticated]);
```

---

## Setup & Installation

### Prerequisites

- **Node.js** 18+ (npm/yarn/pnpm)

### Installation Steps

1. **Navigate to frontend directory:**
   ```bash
   cd medicare-chat
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file:**
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

5. **Access application:**
   - URL: http://localhost:5173

### Build for Production

```bash
npm run build
```

Output in `dist/` folder.

---

## Development Guide

### Running in Development Mode

```bash
npm run dev
```

Features:
- Hot Module Replacement (HMR)
- Fast refresh
- TypeScript type checking
- Port: 5173

### Code Style

- **TypeScript:** Strict mode enabled
- **ESLint:** Configured for React + TypeScript
- **Prettier:** (Optional) Code formatting
- **Naming:** PascalCase for components, camelCase for functions

### Adding New Component

1. **Create component file:**
   ```typescript
   // src/components/MyComponent.tsx
   interface MyComponentProps {
     title: string;
   }

   export const MyComponent = ({ title }: MyComponentProps) => {
     return <div>{title}</div>;
   };
   ```

2. **Import and use:**
   ```typescript
   import { MyComponent } from '@/components/MyComponent';
   
   <MyComponent title="Hello" />
   ```

### Adding Shadcn/ui Component

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add tabs
```

Components added to `src/components/ui/`

### Type Definitions (`types/chat.ts`)

```typescript
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  attachments?: Attachment[];
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface UserProfile {
  user_id: string;
  email: string;
  full_name: string;
  created_at: string;
  age?: number;
  gender?: string;
  health_summary?: string;
  medical_conditions?: string[];
}

export interface Document {
  document_id: string;
  user_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  description?: string;
  extracted_text?: string;
  processed: boolean;
  uploaded_at: string;
}
```

---

## Styling

### Tailwind CSS

Utility-first CSS framework:
```tsx
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Click Me
</button>
```

### Custom Styles (`index.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --primary: 222.2 47.4% 11.2%;
    --background: 0 0% 100%;
    /* ... more CSS variables */
  }
}
```

### Dark Mode

Automatic dark mode support via Tailwind:
```tsx
<div className="bg-white dark:bg-gray-900">
  Content
</div>
```

---

## Performance Optimization

### Code Splitting

Vite automatically splits code by routes.

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react';

const ProfileModal = lazy(() => import('./ProfileModal'));

<Suspense fallback={<div>Loading...</div>}>
  <ProfileModal />
</Suspense>
```

### Memoization

```typescript
import { useMemo, useCallback } from 'react';

const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

const handleClick = useCallback(() => {
  // Handle click
}, [dependency]);
```

---

## Testing

### Run Tests

```bash
npm run test
```

### Testing Framework

- **Vitest** - Unit testing
- **Testing Library** - Component testing

---

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Environment Variables

Set in hosting platform:
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## Troubleshooting

### Common Issues

**CORS Error:**
- Check backend CORS settings
- Ensure API_BASE_URL is correct

**Authentication Not Working:**
- Check token in localStorage
- Verify backend `/users/me` endpoint

**Components Not Rendering:**
- Check TypeScript errors
- Verify imports (use `@/` alias)

**Build Errors:**
- Clear cache: `rm -rf node_modules/.vite`
- Reinstall: `npm install`

---

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile: iOS 12+, Android 8+

---

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support

---

## License

[Your License Here]

---

**Frontend Status: ✅ Production Ready**
