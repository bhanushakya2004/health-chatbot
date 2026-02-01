"""
Enhanced MongoDB Seed Script
Creates ONE test user with rich chat history, documents, and health reports
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

# Test User Credentials
TEST_USER = {
    "email": "john@test.com",
    "password": "Test123!",
    "full_name": "John Smith"
}

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

def seed_database():
    """Seed MongoDB with rich test data for ONE user"""
    
    print("\n" + "="*60)
    print("🌱 SEEDING ENHANCED DATABASE")
    print("="*60)
    print(f"📍 MongoDB: {MONGODB_URL}")
    print(f"📍 Database: {DATABASE_NAME}\n")
    
    # Connect
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Test connection
    try:
        client.server_info()
        print("✅ Connected to MongoDB\n")
    except Exception as e:
        print(f"❌ Error: Cannot connect to MongoDB: {e}")
        print("\nMake sure MongoDB is running:")
        print("  mongod\n")
        return
    
    # Create User
    print("👤 Creating test user...")
    user_id = "U1A2B3C4"
    
    # Clear existing test user data
    db.users.delete_many({"user_id": user_id})
    db.chats.delete_many({"user_id": user_id})
    db.reports.delete_many({"patient_id": user_id})
    db.documents.delete_many({"user_id": user_id})
    
    user_doc = {
        "user_id": user_id,
        "email": TEST_USER["email"],
        "full_name": TEST_USER["full_name"],
        "hashed_password": hash_password(TEST_USER["password"]),
        "created_at": datetime.now() - timedelta(days=60),
        "age": 35,
        "gender": "Male",
        "health_summary": """**Chronic Conditions:**
- Type 2 Diabetes (diagnosed 2 years ago)
- Mild Hypertension

**Current Medications:**
- Metformin 500mg twice daily
- Lisinopril 10mg once daily

**Allergies:**
- Penicillin (rash reaction)

**Lifestyle:**
- Non-smoker
- Occasional alcohol consumption
- Exercises 3x per week
- BMI: 28 (slightly overweight)

**Recent Concerns:**
- Experiencing occasional dizziness
- Blood sugar levels slightly elevated in morning
- Mild knee pain after exercise""",
        "medical_conditions": ["Type 2 Diabetes", "Hypertension"],
        "last_summary_update": datetime.now() - timedelta(days=5)
    }
    
    db.users.insert_one(user_doc)
    print(f"   ✅ User: {TEST_USER['email']}")
    
    # Create Chat History
    print("\n💬 Creating chat conversations...")
    
    chats = [
        {
            "id": "C1234567",
            "user_id": user_id,
            "title": "Blood Sugar Management",
            "messages": [
                {
                    "id": "M001",
                    "role": "user",
                    "content": "My morning blood sugar has been around 140-150 mg/dL consistently. Should I be worried?",
                    "timestamp": datetime.now() - timedelta(days=10, hours=9)
                },
                {
                    "id": "M002",
                    "role": "assistant",
                    "content": """I understand your concern about your fasting blood sugar levels. For someone with Type 2 Diabetes like yourself, the target fasting blood sugar is typically 80-130 mg/dL, so your readings of 140-150 mg/dL are slightly elevated.

**Here's what I recommend:**

1. **Monitor Consistently** - Track your readings for the next week at the same time each morning
2. **Review Evening Meals** - High-carb dinners can affect morning readings
3. **Medication Timing** - Since you're on Metformin 500mg twice daily, discuss timing with your doctor
4. **Evening Activity** - A light 15-minute walk after dinner can help
5. **Stay Hydrated** - Dehydration can raise blood sugar

Given your current medication regimen, if readings consistently stay above 140 mg/dL, consult your doctor about possibly adjusting your Metformin dosage.

**Important:** Don't skip or change medication without medical advice. Keep monitoring and keep me updated!""",
                    "timestamp": datetime.now() - timedelta(days=10, hours=8, minutes=58)
                },
                {
                    "id": "M003",
                    "role": "user",
                    "content": "Thank you! Should I completely avoid rice at dinner?",
                    "timestamp": datetime.now() - timedelta(days=10, hours=8, minutes=45)
                },
                {
                    "id": "M004",
                    "role": "assistant",
                    "content": """You don't need to avoid rice completely! The key is **portion control** and **choosing wisely**:

**Better Choices:**
- Brown rice or basmati (lower glycemic index)
- Maximum ½ cup cooked rice
- Pair with protein (chicken/fish) and lots of vegetables
- Eat earlier (ideally before 7 PM)

**Sample Balanced Dinner:**
- ½ cup brown rice
- 4 oz grilled chicken/fish
- 2 cups mixed vegetables
- Small salad

This balanced approach helps control blood sugar while keeping meals enjoyable. Track your morning readings and see how they respond!""",
                    "timestamp": datetime.now() - timedelta(days=10, hours=8, minutes=47)
                }
            ],
            "created_at": datetime.now() - timedelta(days=10, hours=9),
            "updated_at": datetime.now() - timedelta(days=10, hours=8, minutes=47)
        },
        {
            "id": "C2345678",
            "user_id": user_id,
            "title": "Exercise and Knee Pain",
            "messages": [
                {
                    "id": "M005",
                    "role": "user",
                    "content": "I've been experiencing knee pain after jogging. Should I stop exercising?",
                    "timestamp": datetime.now() - timedelta(days=5, hours=16)
                },
                {
                    "id": "M006",
                    "role": "assistant",
                    "content": """**Don't stop exercising!** It's crucial for managing your diabetes. Let's modify your routine instead:

**Low-Impact Alternatives:**
1. **Swimming** - Excellent for diabetes, zero joint impact
2. **Cycling** - Indoor or outdoor
3. **Elliptical machine** - Easier on knees than jogging
4. **Brisk walking** - 30-45 minutes daily

**For Knee Health:**
- Strengthen supporting muscles (leg lifts, wall sits)
- Proper footwear with good cushioning
- Always warm up and cool down
- Ice after exercise if needed

**Consider:**
Your BMI of 28 puts extra stress on your knees. Even modest weight loss (10-15 lbs) would help significantly.

**See a doctor if:**
- Pain persists > 2 weeks
- Swelling occurs
- Pain worsens

Given your hypertension, maintaining regular exercise is important. Let's find activities that work for your body!""",
                    "timestamp": datetime.now() - timedelta(days=5, hours=15, minutes=58)
                },
                {
                    "id": "M007",
                    "role": "user",
                    "content": "That makes sense. What about swimming - how often should I swim?",
                    "timestamp": datetime.now() - timedelta(days=5, hours=15, minutes=45)
                },
                {
                    "id": "M008",
                    "role": "assistant",
                    "content": """Swimming is excellent for you! Here's an ideal schedule:

**Frequency:**
- **Start:** 2-3 times per week
- **Duration:** 20-30 minutes per session
- **Goal:** Work up to 45 minutes, 3-4x/week

**Benefits for Your Conditions:**
- Helps control blood sugar for up to 24 hours
- Lowers blood pressure
- Zero impact on knees
- Burns calories for weight management
- Improves cardiovascular health

**Swimming Plan:**
- Week 1-2: 20 minutes, 3x/week
- Week 3-4: 30 minutes, 3x/week
- Week 5+: 30-45 minutes, 3-4x/week

**Pro Tips:**
- Swim 1-2 hours after meals
- Stay hydrated (yes, even in the pool!)
- Monitor blood sugar before/after
- Mix different strokes for full-body workout

This will be great for both your diabetes and blood pressure management!""",
                    "timestamp": datetime.now() - timedelta(days=5, hours=15, minutes=47)
                }
            ],
            "created_at": datetime.now() - timedelta(days=5, hours=16),
            "updated_at": datetime.now() - timedelta(days=5, hours=15, minutes=47)
        },
        {
            "id": "C3456789",
            "user_id": user_id,
            "title": "Dizziness and Medication",
            "messages": [
                {
                    "id": "M009",
                    "role": "user",
                    "content": "I've been feeling dizzy when I stand up quickly, especially in the morning. Is this related to my blood pressure medication (Lisinopril)?",
                    "timestamp": datetime.now() - timedelta(days=2, hours=10)
                },
                {
                    "id": "M010",
                    "role": "assistant",
                    "content": """This sounds like **orthostatic hypotension** (sudden blood pressure drop when standing), which can be related to your Lisinopril. Let me help you understand:

**Possible Causes:**
1. **Medication effect** - Lisinopril can sometimes lower BP too much
2. **Dehydration** - Common with diabetes
3. **Blood sugar fluctuations**

**Immediate Safety Tips:**
1. **Stand up SLOWLY** - Sit on bed edge for 30 seconds first
2. **Stay hydrated** - Drink 8-10 glasses water daily
3. **Monitor BP** - Check it sitting and standing
4. **Check blood sugar** - When dizzy, test your glucose

**⚠️ IMPORTANT - Schedule Doctor Visit Soon:**

**Track this for your doctor:**
- When dizziness occurs (time of day)
- How long it lasts
- Your BP readings (sitting vs standing)
- Your blood sugar at those times

**Emergency Signs (go to ER):**
- Severe dizziness with chest pain
- Fainting
- Severe headache
- Vision changes

**DO NOT skip your medication** - Continue as prescribed. Your doctor can safely adjust dosage if needed.""",
                    "timestamp": datetime.now() - timedelta(days=2, hours=9, minutes=58)
                },
                {
                    "id": "M011",
                    "role": "user",
                    "content": "Thank you. One more question - should I take my BP medication at a different time of day?",
                    "timestamp": datetime.now() - timedelta(days=2, hours=9, minutes=45)
                },
                {
                    "id": "M012",
                    "role": "assistant",
                    "content": """**⚠️ Do NOT change medication timing without consulting your doctor first.**

However, here are some considerations to discuss with them:

**Timing Options:**
1. **Morning (current)** - Standard timing for Lisinopril
2. **Evening** - May help if morning dizziness is the main issue
3. **Split dose** - Sometimes prescribed as smaller doses 2x/day

**What to discuss with your doctor:**
- Your dizziness pattern (timing, severity)
- Your BP readings throughout the day
- Whether evening dosing might help
- If current dose (10mg) needs adjustment

**Before Your Appointment:**
- Take BP readings 2-3 times daily (morning, afternoon, evening)
- Note when dizziness occurs
- Keep a log for 3-5 days

**In the meantime:**
- Continue your current schedule
- Follow the safety tips I mentioned
- Stay well-hydrated
- Avoid sudden position changes

Call your doctor's office today to schedule an appointment within the next few days. This is important but not an emergency if you're following safety precautions.""",
                    "timestamp": datetime.now() - timedelta(days=2, hours=9, minutes=47)
                }
            ],
            "created_at": datetime.now() - timedelta(days=2, hours=10),
            "updated_at": datetime.now() - timedelta(days=2, hours=9, minutes=47)
        },
        {
            "id": "C4567890",
            "user_id": user_id,
            "title": "Diet and Nutrition Questions",
            "messages": [
                {
                    "id": "M013",
                    "role": "user",
                    "content": "What's the best diet for managing both diabetes and blood pressure?",
                    "timestamp": datetime.now() - timedelta(hours=6)
                },
                {
                    "id": "M014",
                    "role": "assistant",
                    "content": """Perfect question! For managing both conditions, I recommend a **DASH + Mediterranean hybrid diet**:

**🥗 Focus On:**

**Lean Proteins:**
- Fish (especially salmon, tuna) 2-3x/week
- Skinless chicken breast
- Legumes and beans
- Low-fat dairy
- Eggs (limit to 4-5/week)

**Whole Grains:**
- Oats
- Quinoa
- Brown rice (½ cup portions)
- Whole wheat bread (2 slices max)

**Vegetables (Unlimited):**
- Leafy greens
- Broccoli, cauliflower
- Bell peppers
- Tomatoes
- Cucumbers

**Healthy Fats:**
- Olive oil (2-3 tbsp daily)
- Nuts (1 handful) - almonds, walnuts
- Avocado (½ per day)

**Fruits (2-3 servings):**
- Berries (best for diabetes)
- Apples
- Citrus fruits

**⚠️ Limit or Avoid:**
- Sodium < 2000mg/day (for BP)
- Refined sugars and sweets
- White bread, white rice
- Processed foods
- Saturated fats
- Red meat (once a week max)
- Alcohol (limit to 1 drink/day)

**💧 Hydration:**
- 8-10 glasses water daily
- Limit caffeine
- Avoid sugary drinks completely

**🍽️ Eating Pattern:**
- 3 balanced meals
- 2 small snacks (if needed)
- NEVER skip breakfast
- Dinner before 7 PM

Would you like me to create a sample weekly meal plan?""",
                    "timestamp": datetime.now() - timedelta(hours=5, minutes=58)
                },
                {
                    "id": "M015",
                    "role": "user",
                    "content": "Yes please! A weekly meal plan would be very helpful.",
                    "timestamp": datetime.now() - timedelta(hours=5, minutes=45)
                },
                {
                    "id": "M016",
                    "role": "assistant",
                    "content": """**7-DAY MEAL PLAN** (Diabetes + Hypertension Friendly)

**MONDAY**
- Breakfast: Steel-cut oatmeal + berries + walnuts
- Snack: Apple slices + 10 almonds
- Lunch: Grilled chicken salad + olive oil dressing
- Snack: Carrot sticks + hummus
- Dinner: Baked salmon + quinoa + steamed broccoli

**TUESDAY**
- Breakfast: Greek yogurt + sliced strawberries
- Snack: Small orange
- Lunch: Lentil soup + whole wheat roll
- Snack: Cucumber slices
- Dinner: Turkey breast + sweet potato + green beans

**WEDNESDAY**
- Breakfast: Scrambled eggs + avocado + whole wheat toast
- Snack: Handful of blueberries
- Lunch: Tuna sandwich (whole wheat) + mixed greens
- Snack: Celery + natural peanut butter
- Dinner: Grilled chicken + brown rice (½ cup) + asparagus

**THURSDAY**
- Breakfast: Smoothie (spinach, berries, protein powder)
- Snack: Pear
- Lunch: Chickpea salad + olive oil
- Snack: Cherry tomatoes
- Dinner: Baked cod + quinoa + roasted Brussels sprouts

**FRIDAY**
- Breakfast: Oatmeal + cinnamon + sliced banana
- Snack: Small handful walnuts
- Lunch: Grilled chicken wrap (whole wheat tortilla)
- Snack: Bell pepper strips
- Dinner: Lean beef (4 oz) + cauliflower mash + salad

**SATURDAY**
- Breakfast: Veggie omelet + whole wheat toast
- Snack: Berries
- Lunch: Greek salad + grilled chicken
- Snack: Apple + almond butter
- Dinner: Shrimp stir-fry + brown rice (½ cup)

**SUNDAY**
- Breakfast: Greek yogurt parfait + granola + berries
- Snack: Orange
- Lunch: Vegetable soup + whole wheat crackers
- Snack: Handful mixed nuts
- Dinner: Baked salmon + roasted vegetables + quinoa

**💡 Tips:**
- Prep veggies on Sunday
- Cook proteins in bulk
- Always have healthy snacks ready
- Drink water before each meal

This plan keeps sodium low, blood sugar stable, and provides sustained energy!""",
                    "timestamp": datetime.now() - timedelta(hours=5, minutes=48)
                }
            ],
            "created_at": datetime.now() - timedelta(hours=6),
            "updated_at": datetime.now() - timedelta(hours=5, minutes=48)
        }
    ]
    
    db.chats.insert_many(chats)
    total_messages = sum(len(chat["messages"]) for chat in chats)
    print(f"   ✅ {len(chats)} conversations with {total_messages} messages")
    
    # Create Medical Reports
    print("\n📋 Creating medical reports...")
    
    reports = [
        {
            "report_id": "R1234567",
            "patient_id": user_id,
            "report_type": "HbA1c Test",
            "doctor_name": "Dr. Sarah Johnson",
            "findings": "HbA1c level measured at 7.2%, showing fair glycemic control. Patient has been managing diabetes for 2 years with Metformin 500mg BID. Morning blood sugar readings have been elevated (140-150 mg/dL). Patient reports consistent medication adherence.",
            "diagnosis": "Type 2 Diabetes Mellitus - Fair Control (Target: < 7.0%)",
            "recommendations": "Consider increasing Metformin to 750mg BID. Dietary counseling recommended focusing on evening carbohydrate intake. Increase physical activity to 150 min/week. Follow-up HbA1c in 3 months.",
            "test_results": {
                "HbA1c": "7.2%",
                "target_range": "< 7.0%",
                "fasting_glucose": "145 mg/dL",
                "random_glucose": "168 mg/dL",
                "interpretation": "Fair control - needs improvement"
            },
            "date": datetime.now() - timedelta(days=20),
            "created_at": datetime.now() - timedelta(days=20),
            "created_by": "DR12345"
        },
        {
            "report_id": "R2345678",
            "patient_id": user_id,
            "report_type": "Blood Pressure Monitoring",
            "doctor_name": "Dr. Michael Chen",
            "findings": "2-week BP monitoring shows average 138/88 mmHg. Patient on Lisinopril 10mg daily. Recent reports of orthostatic dizziness upon standing in mornings. No target organ damage detected. Good medication compliance.",
            "diagnosis": "Essential Hypertension - Stage 1, Adequately Controlled",
            "recommendations": "Continue Lisinopril 10mg daily. Patient education on preventing orthostatic hypotension (slow position changes, adequate hydration). Consider timing adjustment if dizziness persists. Reduce sodium to < 2000mg/day. Home BP monitoring twice daily.",
            "test_results": {
                "systolic_average": "138 mmHg",
                "diastolic_average": "88 mmHg",
                "target": "< 130/80 mmHg",
                "heart_rate": "72 bpm",
                "orthostatic_test": "Positive (15mmHg drop on standing)",
                "status": "Borderline - needs close monitoring"
            },
            "date": datetime.now() - timedelta(days=12),
            "created_at": datetime.now() - timedelta(days=12),
            "created_by": "DR67890"
        },
        {
            "report_id": "R3456789",
            "patient_id": user_id,
            "report_type": "Lipid Panel",
            "doctor_name": "Dr. Sarah Johnson",
            "findings": "Comprehensive metabolic panel: Total cholesterol 210 mg/dL, LDL 135 mg/dL, HDL 42 mg/dL (low), Triglycerides 165 mg/dL (elevated). BMI 28 (overweight). Liver and kidney function normal. Associated with diabetes and hypertension.",
            "diagnosis": "Dyslipidemia - Borderline High Cholesterol",
            "recommendations": "Therapeutic lifestyle changes before statin therapy: 1) Increase HDL through regular exercise (swimming recommended), 2) Reduce LDL through diet (limit saturated fats), 3) Weight loss target 10-15 lbs, 4) Omega-3 supplementation (2g daily). Recheck lipid panel in 6 months.",
            "test_results": {
                "total_cholesterol": "210 mg/dL",
                "LDL": "135 mg/dL",
                "HDL": "42 mg/dL",
                "triglycerides": "165 mg/dL",
                "cholesterol_ratio": "5.0",
                "liver_enzymes": "Normal",
                "kidney_function": "eGFR > 90 (Normal)"
            },
            "date": datetime.now() - timedelta(days=25),
            "created_at": datetime.now() - timedelta(days=25),
            "created_by": "DR12345"
        }
    ]
    
    db.reports.insert_many(reports)
    print(f"   ✅ {len(reports)} detailed reports")
    
    # Create Document Metadata
    print("\n📄 Creating document records...")
    
    documents = [
        {
            "document_id": "D1234567",
            "user_id": user_id,
            "file_id": "gridfs_dummy_001",
            "filename": "HbA1c_Test_Results_Jan2026.pdf",
            "file_type": "application/pdf",
            "file_size": 245678,
            "description": "HbA1c blood test results showing glycemic control at 7.2%",
            "extracted_text": "HbA1c: 7.2% | Fasting Glucose: 145 mg/dL | Test Date: Jan 11, 2026",
            "processed": True,
            "uploaded_at": datetime.now() - timedelta(days=20),
            "title": "HbA1c Test Results",
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=20)
        },
        {
            "document_id": "D2345678",
            "user_id": user_id,
            "file_id": "gridfs_dummy_002",
            "filename": "BP_Monitoring_Log.pdf",
            "file_type": "application/pdf",
            "file_size": 189456,
            "description": "2-week blood pressure monitoring log with morning and evening readings",
            "extracted_text": "Average BP: 138/88 mmHg | Orthostatic drop noted | Date Range: Jan 15-29, 2026",
            "processed": True,
            "uploaded_at": datetime.now() - timedelta(days=12),
            "title": "BP Monitoring Log",
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=12)
        },
        {
            "document_id": "D3456789",
            "user_id": user_id,
            "file_id": "gridfs_dummy_003",
            "filename": "Lipid_Panel_Dec2025.pdf",
            "file_type": "application/pdf",
            "file_size": 198234,
            "description": "Complete lipid panel and metabolic analysis",
            "extracted_text": "Total Cholesterol: 210 | LDL: 135 | HDL: 42 | Triglycerides: 165 mg/dL",
            "processed": True,
            "uploaded_at": datetime.now() - timedelta(days=25),
            "title": "Lipid Panel Results",
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=25)
        },
        {
            "document_id": "D4567890",
            "user_id": user_id,
            "file_id": "gridfs_dummy_004",
            "filename": "Medication_List.pdf",
            "file_type": "application/pdf",
            "file_size": 125890,
            "description": "Current medication list and dosing schedule",
            "extracted_text": "Metformin 500mg BID | Lisinopril 10mg QD | Penicillin Allergy noted",
            "processed": True,
            "uploaded_at": datetime.now() - timedelta(days=30),
            "title": "Current Medications",
            "mime_type": "application/pdf",
            "upload_date": datetime.now() - timedelta(days=30)
        }
    ]
    
    db.documents.insert_many(documents)
    print(f"   ✅ {len(documents)} document records")
    
    # Summary
    print("\n" + "="*60)
    print("✨ DATABASE POPULATED SUCCESSFULLY!")
    print("="*60)
    
    print(f"\n🔐 **LOGIN CREDENTIALS:**")
    print("-" * 60)
    print(f"   📧 Email:    {TEST_USER['email']}")
    print(f"   🔑 Password: {TEST_USER['password']}")
    print("-" * 60)
    
    print(f"\n📊 **DATA SUMMARY:**")
    print(f"   👤 User:           1 ({TEST_USER['full_name']})")
    print(f"   💬 Conversations:  {len(chats)}")
    print(f"   📨 Total Messages: {total_messages}")
    print(f"   📋 Reports:        {len(reports)}")
    print(f"   📄 Documents:      {len(documents)}")
    
    print(f"\n🏥 **HEALTH PROFILE:**")
    print(f"   📌 Age: 35, Male")
    print(f"   📌 Conditions: Type 2 Diabetes, Hypertension")
    print(f"   📌 Medications: Metformin 500mg BID, Lisinopril 10mg QD")
    print(f"   📌 Recent HbA1c: 7.2%")
    print(f"   📌 Recent BP: 138/88 mmHg")
    
    print(f"\n🌐 **NEXT STEPS:**")
    print(f"   1. Make sure backend is running: http://localhost:8000")
    print(f"   2. Open frontend and login with above credentials")
    print(f"   3. You'll see 4 chat conversations with history!")
    print(f"   4. Check Profile → View 3 medical reports")
    print(f"   5. Check Documents → See 4 uploaded files")
    
    print("\n" + "="*60)
    print("💡 TIP: The AI assistant already knows your health history!")
    print("💡 Try asking: 'Based on my reports, should I adjust my diet?'")
    print("="*60 + "\n")
    
    client.close()

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        print("Make sure MongoDB is running:")
        print("  Start MongoDB: mongod")
        print("\nOr check if MongoDB service is active")
