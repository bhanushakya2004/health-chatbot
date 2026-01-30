# Test Credentials for Health Chatbot

## MongoDB Database Info
- **URL**: `mongodb://localhost:27017`
- **Database Name**: `healthcare_db`

---

## User Accounts

### 1. Admin Account
- **Email**: `admin@medihelp.com`
- **Password**: `admin123`
- **Full Name**: Admin User
- **Purpose**: System administration and testing

### 2. Doctor Account
- **Email**: `doctor@medihelp.com`
- **Password**: `doctor123`
- **Full Name**: Dr. Sarah Johnson
- **Purpose**: Healthcare provider account with patient records

### 3. Test Account
- **Email**: `test@example.com`
- **Password**: `test123`
- **Full Name**: Test User
- **Purpose**: General testing and QA

### 4. User Account 1
- **Email**: `john.doe@example.com`
- **Password**: `password123`
- **Full Name**: John Doe
- **Purpose**: Regular user account

### 5. User Account 2
- **Email**: `jane.smith@example.com`
- **Password**: `password123`
- **Full Name**: Jane Smith
- **Purpose**: Regular user account

---

## Sample Data Overview

### Users: 5 accounts
All with bcrypt-hashed passwords, ready for login

### Patients: 5 patient records
- Robert Wilson (45, Male) - Diabetes, Hypertension
- Emily Brown (32, Female) - Asthma
- Michael Chen (58, Male) - High Cholesterol, Arthritis
- Sarah Martinez (27, Female) - Healthy
- David Lee (65, Male) - Chronic Kidney Disease, Gout

### Reports: 3 medical reports
- Blood Test for Robert Wilson
- Pulmonary Function Test for Emily Brown
- Lipid Panel for Michael Chen

### Documents: 3 document records
- Lab report PDF
- Chest X-Ray image
- Prescription PDF

---

## Quick Start

### 1. Seed the Database (First Time Only)

**Windows:**
```bash
seed-database.bat
```

**Linux/Mac:**
```bash
cd healthcare-api
python seed_database.py
```

### 2. Start the Backend
```bash
start-backend.bat
```

### 3. Start the Frontend
```bash
start-frontend.bat
```

### 4. Login
1. Go to http://localhost:5173
2. Use any of the credentials above
3. Start chatting!

---

## Recommended Test Flow

### Test 1: Login with Existing Account
1. Use `test@example.com` / `test123`
2. Verify successful login
3. Test chat functionality

### Test 2: Create New Account
1. Click "Sign up"
2. Create a new account with your email
3. Verify auto-login works

### Test 3: Doctor Account with Patient Data
1. Use `doctor@medihelp.com` / `doctor123`
2. This account has 4 associated patients
3. Can test patient-related features

---

## Database Collections

After seeding, your MongoDB will have:

```
healthcare_db
├── users           (5 documents)
├── patients        (5 documents)
├── reports         (3 documents)
└── documents       (3 documents)
```

---

## Reset Database

To clear and re-seed the database:

```bash
# Run seed script again - it clears existing data first
seed-database.bat
```

Or manually in MongoDB:
```javascript
use healthcare_db
db.users.drop()
db.patients.drop()
db.reports.drop()
db.documents.drop()
```

Then run `seed-database.bat` again.

---

## Security Note

⚠️ **Important**: These are TEST credentials only!
- Do NOT use in production
- Change all passwords for production deployment
- Use strong passwords and proper secret management
- The SECRET_KEY in .env should be changed

---

## Troubleshooting

### "Connection refused" error
**Problem**: MongoDB is not running
**Solution**: 
```bash
mongod
```

### "Database already exists" warning
**Problem**: Running seed script multiple times
**Solution**: This is normal - script clears old data first

### "Module not found" error
**Problem**: Missing Python dependencies
**Solution**:
```bash
cd healthcare-api
pip install -r requirements.txt
```

---

## API Testing

You can also test the API directly:

### Login Request
```bash
curl -X POST http://localhost:8000/login \
  -F "username=test@example.com" \
  -F "password=test123"
```

### Chat Request (with token)
```bash
curl -X POST http://localhost:8000/healthchat \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are symptoms of flu?"}'
```

---

**Last Updated**: 2026-01-30
**MongoDB Version**: 5.0+
**Database**: healthcare_db
