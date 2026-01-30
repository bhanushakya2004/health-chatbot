# Healthcare Consultant API

A comprehensive FastAPI application for managing patient records, medical reports, document uploads, and AI-powered health consultations.

## Features

- 👤 **Patient Management**: Create, read, update, and delete patient records
- 📋 **Medical Reports**: Store and retrieve medical reports and test results
- 📄 **Document Upload**: Upload and manage medical documents (PDFs, images, etc.)
- 🤖 **AI Health Chat**: Get AI-powered health recommendations based on patient data

## Project Structure

```
healthcare-api/
├── app/
│   ├── config/          # Database configuration
│   ├── models/          # Pydantic models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── utils/           # Helper functions
├── uploads/             # File storage
├── requirements.txt
└── .env
```

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd healthcare-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=healthcare_db
UPLOAD_DIR=./uploads/documents
GEMINI_API_KEY=your_api_key_here
```

5. **Run MongoDB**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
```

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Patients
- `POST /patients/` - Create new patient
- `GET /patients/` - Get all patients
- `GET /patients/{patient_id}` - Get patient by ID
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

### Reports
- `POST /reports/` - Create new report
- `GET /reports/patient/{patient_id}` - Get all reports for patient
- `GET /reports/{report_id}` - Get report by ID
- `PUT /reports/{report_id}` - Update report
- `DELETE /reports/{report_id}` - Delete report

### Documents
- `POST /documents/upload` - Upload document
- `GET /documents/patient/{patient_id}` - Get all documents for patient
- `GET /documents/{document_id}` - Get document by ID
- `DELETE /documents/{document_id}` - Delete document

### Health Chat
- `POST /healthchat` - AI-powered health consultation

## Usage Examples

### 1. Create a Patient
```bash
curl -X POST "http://localhost:8000/patients/"
  -H "Content-Type: application/json"
  -d 
  {
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "blood_group": "O+",
    "height": 175.5,
    "weight": 75.0,
    "phone": "+1234567890",
    "email": "john @example.com",
    "health_info": {
      "allergies": ["Penicillin"],
      "chronic_conditions": ["Diabetes Type 2"],
      "current_medications": ["Metformin"]
    }
  }
```

### 2. Add a Medical Report
```bash
curl -X POST "http://localhost:8000/reports/"
  -H "Content-Type: application/json"
  -d 
  {
    "patient_id": "P12345",
    "report_type": "Blood Test",
    "doctor_name": "Dr. Smith",
    "findings": "Blood sugar levels elevated",
    "diagnosis": "Pre-diabetic condition",
    "test_results": {
      "glucose": 120,
      "hemoglobin": 14.5
    }
  }
```

### 3. Upload a Document
```bash
curl -X POST "http://localhost:8000/documents/upload"
  -F "file=@/path/to/document.pdf"
  -F "patient_id=P12345"
  -F "description=X-Ray Report"
```

### 4. Health Chat Consultation
```bash
curl -X POST "http://localhost:8000/healthchat"
  -H "Content-Type: application/json"
  -d 
  {
    "query": "Get the latest report for patient P12345 and provide health recommendations"
  }
```

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Testing

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Technologies

- **FastAPI** - Modern web framework
- **MongoDB** - NoSQL database
- **Agno** - AI agent framework
- **Google Gemini** - Language model
- **Pydantic** - Data validation
- **Python 3.8+**

## License

MIT License

