# Testing Guide

## Pre-Testing Checklist

Before testing, ensure:
- [ ] MongoDB is running (`mongod`)
- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 5173
- [ ] Browser DevTools is open (Console + Network tabs)

## Test Suite

### 1. Authentication Tests

#### Test 1.1: Sign Up (New User)
**Steps:**
1. Open http://localhost:5173
2. You should see "Welcome to MediHelp" screen with auth modal
3. Click "Sign up" link at bottom of modal
4. Fill in the form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
5. Click "Create account"

**Expected Results:**
- ✅ Modal closes
- ✅ Toast notification: "Account created"
- ✅ Chat interface appears (authenticated)
- ✅ Sidebar shows "Log out" button
- ✅ localStorage has `access_token`
- ✅ Backend console shows: POST /signup 201
- ✅ Backend console shows: POST /login 200

**Verification:**
```javascript
// In browser console:
localStorage.getItem('access_token')
// Should return a JWT token like: "eyJhbGc..."
```

#### Test 1.2: Sign Up (Duplicate Email)
**Steps:**
1. Log out if logged in
2. Try signing up again with same email: `test@example.com`

**Expected Results:**
- ❌ Error toast: "Email already registered"
- ❌ User stays on auth modal
- ❌ Not logged in

#### Test 1.3: Login (Existing User)
**Steps:**
1. If logged in, log out first
2. Auth modal should appear
3. Ensure you're on "Sign in" tab
4. Fill in:
   - Email: `test@example.com`
   - Password: `password123`
5. Click "Sign in"

**Expected Results:**
- ✅ Modal closes
- ✅ Toast notification: "Login successful"
- ✅ Chat interface appears
- ✅ Sidebar shows "Log out" button
- ✅ Backend console shows: POST /login 200

#### Test 1.4: Login (Wrong Password)
**Steps:**
1. Log out if logged in
2. Try logging in with:
   - Email: `test@example.com`
   - Password: `wrongpassword`

**Expected Results:**
- ❌ Error toast: "Incorrect email or password"
- ❌ User stays on auth modal
- ❌ Not logged in

#### Test 1.5: Logout
**Steps:**
1. When logged in, click "Log out" in sidebar

**Expected Results:**
- ✅ Redirected to auth screen
- ✅ Auth modal appears
- ✅ localStorage `access_token` is removed
- ✅ Can't access chat interface

#### Test 1.6: Session Persistence
**Steps:**
1. Log in successfully
2. Refresh the page (F5)

**Expected Results:**
- ✅ User stays logged in
- ✅ Chat interface still visible
- ✅ No redirect to login
- ✅ Token still in localStorage

---

### 2. Protected Routes Tests

#### Test 2.1: Access Without Login
**Steps:**
1. Log out if logged in
2. Clear localStorage
3. Navigate to http://localhost:5173

**Expected Results:**
- ✅ See "Welcome to MediHelp" screen
- ✅ Auth modal automatically opens
- ✅ Can't access chat without login

#### Test 2.2: Access With Login
**Steps:**
1. Log in
2. Navigate to http://localhost:5173

**Expected Results:**
- ✅ Chat interface loads
- ✅ No auth modal
- ✅ Can use all features

---

### 3. Chat Functionality Tests

#### Test 3.1: Create New Chat
**Steps:**
1. Log in
2. Click "New Chat" button in sidebar

**Expected Results:**
- ✅ New chat created
- ✅ Welcome message appears
- ✅ Chat input is enabled
- ✅ Chat appears in sidebar history

#### Test 3.2: Send Message (Success)
**Steps:**
1. Create new chat
2. Type: "What are the symptoms of flu?"
3. Press Enter or click Send

**Expected Results:**
- ✅ User message appears immediately
- ✅ Typing indicator shows
- ✅ AI response appears after ~2 seconds
- ✅ Backend console shows: POST /healthchat 200
- ✅ Chat title updates (first message)

**Network Tab Verification:**
```
Request:
  URL: http://localhost:8000/healthchat
  Method: POST
  Headers: Authorization: Bearer eyJhbGc...
  Body: { "message": "What are the symptoms of flu?" }

Response:
  Status: 200 OK
  Body: { "response": "AI generated response..." }
```

#### Test 3.3: Send Message (Backend Down)
**Steps:**
1. Stop the backend server
2. Try sending a message

**Expected Results:**
- ❌ Error toast: "Failed to get response from AI"
- ❌ Error message added to chat
- ✅ User message still visible

#### Test 3.4: Send Message (No Auth Token)
**Steps:**
1. In browser console: `localStorage.removeItem('access_token')`
2. Try sending a message (without refreshing)

**Expected Results:**
- ❌ API call fails with 401
- ❌ Error toast appears
- ❌ Error message in chat

#### Test 3.5: Multiple Messages
**Steps:**
1. Send 3 different messages in same chat
2. Verify each gets a response

**Expected Results:**
- ✅ All messages appear in order
- ✅ All responses appear correctly
- ✅ Timestamps are correct
- ✅ Chat history is maintained

#### Test 3.6: Switch Between Chats
**Steps:**
1. Create 2 different chats
2. Send messages in each
3. Click between chats in sidebar

**Expected Results:**
- ✅ Correct messages shown for each chat
- ✅ Active chat highlighted in sidebar
- ✅ Messages don't mix between chats

---

### 4. UI/UX Tests

#### Test 4.1: Password Visibility Toggle
**Steps:**
1. On login/signup form
2. Click eye icon next to password field

**Expected Results:**
- ✅ Password toggles between visible/hidden
- ✅ Icon changes between eye/eye-off

#### Test 4.2: Loading States
**Steps:**
1. During login/signup, observe button
2. During chat message, observe typing indicator

**Expected Results:**
- ✅ Login/Signup button shows "Please wait..."
- ✅ Button is disabled during request
- ✅ Typing indicator shows during AI response

#### Test 4.3: Empty State
**Steps:**
1. Log in without any active chat

**Expected Results:**
- ✅ Empty state component shows
- ✅ Helpful message displayed
- ✅ "New Chat" button visible

#### Test 4.4: Sidebar Collapse
**Steps:**
1. Click collapse icon in sidebar
2. Click again to expand

**Expected Results:**
- ✅ Sidebar collapses to icons only
- ✅ Chat area expands
- ✅ Icons still functional
- ✅ Expands back to full width

---

### 5. Error Handling Tests

#### Test 5.1: Network Errors
**Steps:**
1. Turn off WiFi/Network
2. Try to log in

**Expected Results:**
- ❌ Error toast with network error message
- ❌ User not logged in

#### Test 5.2: Invalid Email Format
**Steps:**
1. Try signing up with email: `notanemail`

**Expected Results:**
- ❌ HTML5 validation error
- ❌ Can't submit form

#### Test 5.3: Empty Fields
**Steps:**
1. Try submitting login/signup with empty fields

**Expected Results:**
- ❌ HTML5 validation error
- ❌ Can't submit form

---

### 6. Integration Tests

#### Test 6.1: End-to-End User Journey
**Steps:**
1. Open app (logged out)
2. Sign up new account
3. Create new chat
4. Send 3 messages
5. Create another chat
6. Switch between chats
7. Log out
8. Log back in
9. Verify chats still there (in memory for now)

**Expected Results:**
- ✅ All steps work smoothly
- ✅ No console errors
- ✅ All features functional

#### Test 6.2: Token Expiry (Manual Test)
**Steps:**
1. Log in
2. Wait 30+ minutes
3. Try sending a message

**Expected Results:**
- ❌ 401 Unauthorized error
- ❌ Need to log in again

**Note:** For quick test, modify backend ACCESS_TOKEN_EXPIRE_MINUTES to 1

---

## Testing Checklist Summary

### Authentication
- [ ] Sign up with new account
- [ ] Sign up with duplicate email (should fail)
- [ ] Login with correct credentials
- [ ] Login with wrong password (should fail)
- [ ] Logout
- [ ] Session persistence (refresh page)

### Protected Routes
- [ ] Access without login (should show auth)
- [ ] Access with login (should show chat)

### Chat
- [ ] Create new chat
- [ ] Send message successfully
- [ ] Receive AI response
- [ ] Error handling (backend down)
- [ ] Multiple messages in chat
- [ ] Switch between chats

### UI/UX
- [ ] Password visibility toggle
- [ ] Loading states
- [ ] Empty state
- [ ] Sidebar collapse/expand

### Error Handling
- [ ] Network errors
- [ ] Invalid inputs
- [ ] Empty fields

---

## Debugging Tips

### Check Authentication
```javascript
// In browser console:
localStorage.getItem('access_token') // Should return token
```

### Check API Requests
1. Open DevTools → Network tab
2. Filter by "Fetch/XHR"
3. Look for:
   - `/login` - Status 200
   - `/signup` - Status 201
   - `/healthchat` - Status 200

### Check Backend Logs
Backend terminal should show:
```
INFO:     127.0.0.1:XXXXX - "POST /signup HTTP/1.1" 201
INFO:     127.0.0.1:XXXXX - "POST /login HTTP/1.1" 200
INFO:     127.0.0.1:XXXXX - "POST /healthchat HTTP/1.1" 200
```

### Common Issues

**Issue: CORS Error**
- Solution: Ensure backend is running
- Check backend CORS config in main.py

**Issue: 401 Unauthorized**
- Solution: Token expired or invalid
- Log out and log back in

**Issue: Network Error**
- Solution: Backend not running
- Start backend with `start-backend.bat`

**Issue: MongoDB Error**
- Solution: MongoDB not running
- Start MongoDB with `mongod`

---

## Performance Benchmarks

Expected response times:
- Login: < 1s
- Signup: < 1s
- Chat message: 2-5s (depends on AI)
- Page load: < 500ms

---

## Test Results Template

```
Date: ___________
Tester: ___________

Authentication Tests:
[ ] Sign up: PASS / FAIL - Notes: ___________
[ ] Login: PASS / FAIL - Notes: ___________
[ ] Logout: PASS / FAIL - Notes: ___________

Chat Tests:
[ ] Send message: PASS / FAIL - Notes: ___________
[ ] Receive response: PASS / FAIL - Notes: ___________
[ ] Error handling: PASS / FAIL - Notes: ___________

Overall Status: PASS / FAIL
Critical Issues: ___________
```

---

## Automated Testing (Future)

For automated tests, consider:
1. **Frontend**: Vitest + React Testing Library
2. **Backend**: pytest
3. **E2E**: Playwright or Cypress
4. **API**: Postman Collection (already exists!)

---

**Ready to Test!** 🚀

Start with Test 1.1 (Sign Up) and work your way down the list.
