from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from app.models.patient import PatientCreate, PatientUpdate, PatientResponse
from app.models.user import UserResponse
from app.config.database import get_patients_collection
from app.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, current_user: UserResponse = Depends(get_current_user)):
    """Create a new patient record"""
    patients_collection = get_patients_collection()
    
    # Generate unique patient ID
    patient_id = f"P{str(uuid.uuid4().hex[:8]).upper()}"
    
    # Check if phone already exists
    existing = patients_collection.find_one({"phone": patient.phone})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this phone number already exists"
        )
    
    # Create patient document
    patient_doc = {
        "patient_id": patient_id,
        **patient.model_dump(),
        "created_by": current_user["user_id"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    patients_collection.insert_one(patient_doc)
    patient_doc.pop('_id')
    
    return PatientResponse(**patient_doc)

@router.get("/", response_model=List[PatientResponse])
async def get_all_patients(skip: int = 0, limit: int = 100, current_user: UserResponse = Depends(get_current_user)):
    """Get all patients with pagination"""
    patients_collection = get_patients_collection()
    patients = list(patients_collection.find({"created_by": current_user["user_id"]}).skip(skip).limit(limit))
    
    for patient in patients:
        patient.pop('_id')
    
    return [PatientResponse(**patient) for patient in patients]

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get patient by ID"""
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": patient_id, "created_by": current_user["user_id"]})
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {patient_id} not found"
        )
    
    patient.pop('_id')
    return PatientResponse(**patient)

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: str, patient_update: PatientUpdate, current_user: UserResponse = Depends(get_current_user)):
    """Update patient information"""
    patients_collection = get_patients_collection()
    
    # Check if patient exists
    existing = patients_collection.find_one({"patient_id": patient_id, "created_by": current_user["user_id"]})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {patient_id} not found"
        )
    
    # Update patient
    update_data = {k: v for k, v in patient_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now()
    
    patients_collection.update_one(
        {"patient_id": patient_id},
        {"$set": update_data}
    )
    
    # Get updated patient
    updated_patient = patients_collection.find_one({"patient_id": patient_id})
    updated_patient.pop('_id')
    
    return PatientResponse(**updated_patient)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Delete patient record"""
    patients_collection = get_patients_collection()
    
    result = patients_collection.delete_one({"patient_id": patient_id, "created_by": current_user["user_id"]})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {patient_id} not found"
        )
    
    return None
