"""
MongoDB Seed Script for Health Chatbot
Creates sample users, patients, and related data for testing
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import uuid

# Try different password hashing methods
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_BCRYPT = True
    print("✅ Using bcrypt for password hashing")
except Exception as e:
    print(f"⚠️  Warning: bcrypt issue - {e}")
    print("⚠️  Using fallback password hashing...")
    import hashlib
    USE_BCRYPT = False

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "healthcare_db"

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

def hash_password(password: str) -> str:
    """Hash a password using bcrypt or fallback"""
    if USE_BCRYPT:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            print(f"⚠️  bcrypt failed: {e}, using fallback...")
            import hashlib
            return "$fallback$" + hashlib.sha256(password.encode()).hexdigest()
    else:
        import hashlib
        return "$fallback$" + hashlib.sha256(password.encode()).hexdigest()

def create_users():
    """Create sample users"""
    users_collection = db["users"]
    
    # Clear existing users
    users_collection.delete_many({})
    
    users = [
        {
            "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
            "email": "admin@medihelp.com",
            "full_name": "Admin User",
            "hashed_password": hash_password("admin123"),
            "created_at": datetime.now(),
        },
        {
            "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
            "email": "doctor@medihelp.com",
            "full_name": "Dr. Sarah Johnson",
            "hashed_password": hash_password("doctor123"),
            "created_at": datetime.now(),
        },
        {
            "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
            "email": "test@example.com",
            "full_name": "Test User",
            "hashed_password": hash_password("test123"),
            "created_at": datetime.now() - timedelta(days=30),
        },
        {
            "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
            "email": "john.doe@example.com",
            "full_name": "John Doe",
            "hashed_password": hash_password("password123"),
            "created_at": datetime.now() - timedelta(days=15),
        },
        {
            "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
            "email": "jane.smith@example.com",
            "full_name": "Jane Smith",
            "hashed_password": hash_password("password123"),
            "created_at": datetime.now() - timedelta(days=7),
        }
    ]
    
    result = users_collection.insert_many(users)
    print(f"✅ Created {len(result.inserted_ids)} users")
    return users

def create_patients(users):
    """Create sample patients"""
    patients_collection = db["patients"]
    
    # Clear existing patients
    patients_collection.delete_many({})
    
    patients = [
        {
            "patient_id": f"P{str(uuid.uuid4().hex[:8]).upper()}",
            "name": "Robert Wilson",
            "age": 45,
            "gender": "Male",
            "blood_group": "A+",
            "height": 178.5,
            "weight": 82.0,
            "phone": "+1234567890",
            "email": "robert.wilson@email.com",
            "address": "123 Main St, New York, NY 10001",
            "emergency_contact": "+1234567899",
            "health_info": {
                "allergies": ["Penicillin", "Peanuts"],
                "chronic_conditions": ["Hypertension", "Type 2 Diabetes"],
                "current_medications": ["Metformin 500mg", "Lisinopril 10mg"],
                "previous_surgeries": ["Appendectomy (2015)"],
                "family_history": ["Father: Heart Disease", "Mother: Diabetes"]
            },
            "created_by": users[1]["user_id"],  # Dr. Sarah Johnson
            "created_at": datetime.now() - timedelta(days=60),
            "updated_at": datetime.now() - timedelta(days=5),
        },
        {
            "patient_id": f"P{str(uuid.uuid4().hex[:8]).upper()}",
            "name": "Emily Brown",
            "age": 32,
            "gender": "Female",
            "blood_group": "O-",
            "height": 165.0,
            "weight": 58.5,
            "phone": "+1234567891",
            "email": "emily.brown@email.com",
            "address": "456 Oak Ave, Los Angeles, CA 90001",
            "emergency_contact": "+1234567892",
            "health_info": {
                "allergies": ["Latex"],
                "chronic_conditions": ["Asthma"],
                "current_medications": ["Albuterol Inhaler"],
                "previous_surgeries": [],
                "family_history": ["Sister: Asthma"]
            },
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=45),
            "updated_at": datetime.now() - timedelta(days=10),
        },
        {
            "patient_id": f"P{str(uuid.uuid4().hex[:8]).upper()}",
            "name": "Michael Chen",
            "age": 58,
            "gender": "Male",
            "blood_group": "B+",
            "height": 172.0,
            "weight": 88.0,
            "phone": "+1234567893",
            "email": "michael.chen@email.com",
            "address": "789 Elm St, Chicago, IL 60601",
            "emergency_contact": "+1234567894",
            "health_info": {
                "allergies": ["Sulfa drugs"],
                "chronic_conditions": ["High Cholesterol", "Arthritis"],
                "current_medications": ["Atorvastatin 20mg", "Ibuprofen 400mg"],
                "previous_surgeries": ["Knee Replacement (2020)"],
                "family_history": ["Father: Stroke", "Mother: High Cholesterol"]
            },
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=90),
            "updated_at": datetime.now() - timedelta(days=2),
        },
        {
            "patient_id": f"P{str(uuid.uuid4().hex[:8]).upper()}",
            "name": "Sarah Martinez",
            "age": 27,
            "gender": "Female",
            "blood_group": "AB+",
            "height": 160.0,
            "weight": 55.0,
            "phone": "+1234567895",
            "email": "sarah.martinez@email.com",
            "address": "321 Pine Rd, Houston, TX 77001",
            "emergency_contact": "+1234567896",
            "health_info": {
                "allergies": [],
                "chronic_conditions": [],
                "current_medications": [],
                "previous_surgeries": [],
                "family_history": []
            },
            "created_by": users[2]["user_id"],  # Test User
            "created_at": datetime.now() - timedelta(days=20),
            "updated_at": datetime.now() - timedelta(days=1),
        },
        {
            "patient_id": f"P{str(uuid.uuid4().hex[:8]).upper()}",
            "name": "David Lee",
            "age": 65,
            "gender": "Male",
            "blood_group": "O+",
            "height": 175.0,
            "weight": 78.0,
            "phone": "+1234567897",
            "email": "david.lee@email.com",
            "address": "654 Maple Dr, Phoenix, AZ 85001",
            "emergency_contact": "+1234567898",
            "health_info": {
                "allergies": ["Codeine"],
                "chronic_conditions": ["Chronic Kidney Disease", "Gout"],
                "current_medications": ["Allopurinol 300mg", "Lisinopril 5mg"],
                "previous_surgeries": ["Cataract Surgery (2022)", "Hernia Repair (2018)"],
                "family_history": ["Father: Kidney Disease", "Mother: Gout"]
            },
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=120),
            "updated_at": datetime.now(),
        }
    ]
    
    result = patients_collection.insert_many(patients)
    print(f"✅ Created {len(result.inserted_ids)} patients")
    return patients

def create_reports(patients, users):
    """Create sample medical reports"""
    reports_collection = db["reports"]
    
    # Clear existing reports
    reports_collection.delete_many({})
    
    reports = [
        {
            "report_id": f"R{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[0]["patient_id"],
            "report_type": "Blood Test",
            "report_date": datetime.now() - timedelta(days=30),
            "diagnosis": "Type 2 Diabetes - Controlled, Hypertension - Stable",
            "findings": {
                "Glucose (Fasting)": "126 mg/dL",
                "HbA1c": "6.8%",
                "Blood Pressure": "135/85 mmHg",
                "Cholesterol": "195 mg/dL"
            },
            "recommendations": [
                "Continue current medications",
                "Monitor blood sugar daily",
                "Reduce sodium intake",
                "Exercise 30 minutes daily"
            ],
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=30),
            "updated_at": datetime.now() - timedelta(days=30),
        },
        {
            "report_id": f"R{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[1]["patient_id"],
            "report_type": "Pulmonary Function Test",
            "report_date": datetime.now() - timedelta(days=15),
            "diagnosis": "Mild Persistent Asthma",
            "findings": {
                "FEV1": "82% predicted",
                "Peak Flow": "380 L/min",
                "Reversibility": "15% improvement after bronchodilator"
            },
            "recommendations": [
                "Continue albuterol as needed",
                "Consider inhaled corticosteroid",
                "Avoid triggers",
                "Follow-up in 3 months"
            ],
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=15),
            "updated_at": datetime.now() - timedelta(days=15),
        },
        {
            "report_id": f"R{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[2]["patient_id"],
            "report_type": "Lipid Panel",
            "report_date": datetime.now() - timedelta(days=7),
            "diagnosis": "Dyslipidemia - Improving",
            "findings": {
                "Total Cholesterol": "215 mg/dL",
                "LDL": "135 mg/dL",
                "HDL": "45 mg/dL",
                "Triglycerides": "175 mg/dL"
            },
            "recommendations": [
                "Continue Atorvastatin",
                "Low-fat diet",
                "Increase physical activity",
                "Recheck in 6 months"
            ],
            "created_by": users[1]["user_id"],
            "created_at": datetime.now() - timedelta(days=7),
            "updated_at": datetime.now() - timedelta(days=7),
        }
    ]
    
    result = reports_collection.insert_many(reports)
    print(f"✅ Created {len(result.inserted_ids)} reports")

def create_documents(patients, users):
    """Create sample document metadata"""
    documents_collection = db["documents"]
    
    # Clear existing documents
    documents_collection.delete_many({})
    
    documents = [
        {
            "document_id": f"D{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[0]["patient_id"],
            "document_type": "Lab Report",
            "title": "Blood Test Results - Dec 2025",
            "file_name": "blood_test_dec_2025.pdf",
            "file_size": 245760,  # bytes
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=30),
            "uploaded_by": users[1]["user_id"],
        },
        {
            "document_id": f"D{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[1]["patient_id"],
            "document_type": "X-Ray",
            "title": "Chest X-Ray",
            "file_name": "chest_xray.jpg",
            "file_size": 1048576,
            "mime_type": "image/jpeg",
            "upload_date": datetime.now() - timedelta(days=15),
            "uploaded_by": users[1]["user_id"],
        },
        {
            "document_id": f"D{str(uuid.uuid4().hex[:8]).upper()}",
            "patient_id": patients[2]["patient_id"],
            "document_type": "Prescription",
            "title": "Atorvastatin Prescription",
            "file_name": "prescription_atorvastatin.pdf",
            "file_size": 102400,
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=90),
            "uploaded_by": users[1]["user_id"],
        }
    ]
    
    result = documents_collection.insert_many(documents)
    print(f"✅ Created {len(result.inserted_ids)} documents")

def main():
    """Main seed function"""
    print("=" * 50)
    print("🌱 Seeding MongoDB Database")
    print("=" * 50)
    print()
    
    try:
        # Test connection
        client.server_info()
        print(f"✅ Connected to MongoDB: {MONGODB_URL}")
        print(f"✅ Database: {DATABASE_NAME}")
        print()
        
        # Create data
        users = create_users()
        patients = create_patients(users)
        create_reports(patients, users)
        create_documents(patients, users)
        
        print()
        print("=" * 50)
        print("✅ Database seeding completed successfully!")
        print("=" * 50)
        print()
        print("📋 TEST CREDENTIALS:")
        print("-" * 50)
        print()
        print("1. Admin Account:")
        print("   Email: admin@medihelp.com")
        print("   Password: admin123")
        print()
        print("2. Doctor Account:")
        print("   Email: doctor@medihelp.com")
        print("   Password: doctor123")
        print()
        print("3. Test Account:")
        print("   Email: test@example.com")
        print("   Password: test123")
        print()
        print("4. User Account 1:")
        print("   Email: john.doe@example.com")
        print("   Password: password123")
        print()
        print("5. User Account 2:")
        print("   Email: jane.smith@example.com")
        print("   Password: password123")
        print()
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Make sure MongoDB is running:")
        print("  mongod")
    finally:
        client.close()

if __name__ == "__main__":
    main()
