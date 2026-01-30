from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status, Depends
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
from app.models.document import DocumentResponse
from app.models.user import UserResponse
from app.config.database import get_documents_collection, get_patients_collection
from app.services.storage_service import StorageService
from app.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    description: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user)
):
    """Upload a document for a patient"""
    patients_collection = get_patients_collection()
    documents_collection = get_documents_collection()
    
    # Verify patient exists
    patient = patients_collection.find_one({"patient_id": patient_id, "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {patient_id} not found"
        )
    
    # Save file to GridFS
    file_info = await StorageService.save_file(file, patient_id)
    
    # Generate document ID
    document_id = f"D{str(uuid.uuid4().hex[:8]).upper()}"
    
    # Create document record
    document_doc = {
        "document_id": document_id,
        "patient_id": patient_id,
        "file_id": file_info["file_id"],
        "filename": file_info["filename"],
        "file_type": file_info["file_type"],
        "file_size": file_info["file_size"],
        "description": description,
        "uploaded_at": datetime.now()
    }
    
    documents_collection.insert_one(document_doc)
    document_doc.pop('_id')
    
    return DocumentResponse(**document_doc)

@router.get("/patient/{patient_id}", response_model=List[DocumentResponse])
async def get_patient_documents(patient_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all documents for a specific patient"""
    documents_collection = get_documents_collection()
    documents = list(documents_collection.find({"patient_id": patient_id}).sort("uploaded_at", -1))
    
    if not documents:
        return []
    
    for doc in documents:
        doc.pop('_id')
    
    return [DocumentResponse(**doc) for doc in documents]

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get document by ID"""
    documents_collection = get_documents_collection()
    document = documents_collection.find_one({"document_id": document_id})
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )
    
    document.pop('_id')
    return DocumentResponse(**document)

@router.get("/download/{document_id}")
async def download_document(document_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Download a document"""
    documents_collection = get_documents_collection()
    document = documents_collection.find_one({"document_id": document_id})

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )
        
    # Check if the user has access to the patient associated with the document
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": document["patient_id"], "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this document"
        )

    file = StorageService.get_file(document["file_id"])
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return StreamingResponse(file, media_type=file.content_type, headers={"Content-Disposition": f"attachment; filename={file.filename}"})

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Delete document"""
    documents_collection = get_documents_collection()
    
    # Get document to delete file
    document = documents_collection.find_one({"document_id": document_id})
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )

    # Check if the user has access to the patient associated with the document
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": document["patient_id"], "created_by": current_user["user_id"]})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this document"
        )
    
    # Delete file from storage
    StorageService.delete_file(document["file_id"])
    
    # Delete document record
    documents_collection.delete_one({"document_id": document_id})
    
    return None
