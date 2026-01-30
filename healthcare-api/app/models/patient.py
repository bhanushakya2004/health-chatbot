from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re

class PatientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    gender: str
    blood_group: Optional[str] = None
    height: Optional[float] = Field(default=None, gt=0)  # in cm
    weight: Optional[float] = Field(default=None, gt=0)  # in kg
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(r"^\+?[1-9]\d{1,14}$", v):
            raise ValueError('Invalid phone number format')
        return v

class PatientHealthInfo(BaseModel):
    allergies: Optional[List[str]] = []
    chronic_conditions: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    previous_surgeries: Optional[List[str]] = []
    family_history: Optional[List[str]] = []

class PatientCreate(PatientBase):
    health_info: Optional[PatientHealthInfo] = PatientHealthInfo()

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    health_info: Optional[PatientHealthInfo] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None and not re.match(r"^\+?[1-9]\d{1,14}$", v):
            raise ValueError('Invalid phone number format')
        return v

class PatientResponse(PatientBase):
    patient_id: str
    health_info: PatientHealthInfo
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P12345",
                "name": "John Doe",
                "age": 35,
                "gender": "Male",
                "blood_group": "O+",
                "height": 175.5,
                "weight": 75.0,
                "phone": "+1234567890",
                "email": "john.doe@example.com",
                "health_info": {
                    "allergies": ["Penicillin"],
                    "chronic_conditions": ["Diabetes Type 2"],
                    "current_medications": ["Metformin"]
                },
                "created_by": "U12345678"
            }
        }