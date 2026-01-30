from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from app.models.report import ReportCreate, ReportUpdate, ReportResponse
from app.models.user import UserResponse
from app.config.database import get_reports_collection, get_patients_collection
from app.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(report: ReportCreate, current_user: UserResponse = Depends(get_current_user)):
    """Create a new medical report"""
    patients_collection = get_patients_collection()
    reports_collection = get_reports_collection()
    
    # Verify patient exists and belongs to the current user
    patient = patients_collection.find_one({"patient_id": report.patient_id, "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {report.patient_id} not found"
        )
    
    # Generate unique report ID
    report_id = f"R{str(uuid.uuid4().hex[:8]).upper()}"
    
    # Create report document
    report_doc = {
        "report_id": report_id,
        **report.model_dump(),
        "date": datetime.now(),
        "created_at": datetime.now(),
        "created_by": current_user["user_id"]
    }
    
    reports_collection.insert_one(report_doc)
    report_doc.pop('_id')
    
    return ReportResponse(**report_doc)

@router.get("/patient/{patient_id}", response_model=List[ReportResponse])
async def get_patient_reports(patient_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all reports for a specific patient"""
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": patient_id, "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {patient_id} not found"
        )

    reports_collection = get_reports_collection()
    reports = list(reports_collection.find({"patient_id": patient_id}).sort("date", -1))
    
    if not reports:
        return []
    
    for report in reports:
        report.pop('_id')
    
    return [ReportResponse(**report) for report in reports]

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get report by ID"""
    reports_collection = get_reports_collection()
    report = reports_collection.find_one({"report_id": report_id})
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )

    # Check if the user has access to the patient associated with the report
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": report["patient_id"], "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this report"
        )
    
    report.pop('_id')
    return ReportResponse(**report)

@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(report_id: str, report_update: ReportUpdate, current_user: UserResponse = Depends(get_current_user)):
    """Update report information"""
    reports_collection = get_reports_collection()
    
    # Check if report exists
    existing = reports_collection.find_one({"report_id": report_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )

    # Check if the user has access to the patient associated with the report
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": existing["patient_id"], "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this report"
        )
    
    # Update report
    update_data = {k: v for k, v in report_update.model_dump().items() if v is not None}
    
    reports_collection.update_one(
        {"report_id": report_id},
        {"$set": update_data}
    )
    
    # Get updated report
    updated_report = reports_collection.find_one({"report_id": report_id})
    updated_report.pop('_id')
    
    return ReportResponse(**updated_report)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Delete report"""
    reports_collection = get_reports_collection()
    
    existing = reports_collection.find_one({"report_id": report_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )

    # Check if the user has access to the patient associated with the report
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": existing["patient_id"], "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this report"
        )

    result = reports_collection.delete_one({"report_id": report_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    return None
