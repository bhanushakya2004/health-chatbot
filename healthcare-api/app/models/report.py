from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ReportCreate(BaseModel):
    patient_id: str
    report_type: str = Field(..., min_length=3, max_length=50)
    doctor_name: str = Field(..., min_length=3, max_length=50)
    findings: str = Field(..., min_length=10)
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = {}
    
class ReportUpdate(BaseModel):
    report_type: Optional[str] = Field(default=None, min_length=3, max_length=50)
    doctor_name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    findings: Optional[str] = Field(default=None, min_length=10)
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    report_id: str
    patient_id: str
    report_type: str
    doctor_name: str
    findings: str
    diagnosis: Optional[str]
    recommendations: Optional[str]
    test_results: Dict[str, Any]
    date: datetime
    created_at: datetime
    created_by: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "R12345",
                "patient_id": "P12345",
                "report_type": "Blood Test",
                "doctor_name": "Dr. Smith",
                "findings": "Blood sugar levels elevated",
                "diagnosis": "Pre-diabetic condition",
                "test_results": {
                    "glucose": 120,
                    "hemoglobin": 14.5
                },
                "created_by": "U12345678"
            }
        }