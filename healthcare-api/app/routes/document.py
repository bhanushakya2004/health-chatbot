from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
from app.models.document import DocumentResponse
from app.models.user import UserResponse
from app.config.database import get_documents_collection
from app.services.storage_service import StorageService
from app.services.ocr_service import OCRService
from app.services.context_builder import ContextBuilderService
from app.dependencies import get_current_user
import uuid
import os
import tempfile

router = APIRouter(prefix="/documents", tags=["Documents"])

async def process_document_ocr(document_id: str, file_id: str, filename: str, file_type: str, user_id: str):
    """Background task to process OCR and add to vector store"""
    try:
        documents_collection = get_documents_collection()
        
        # Get file from storage
        file_data = StorageService.get_file(file_id)
        if not file_data:
            print(f"File not found for document {document_id}")
            return
        
        # Save to temporary file for OCR processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(file_data.read())
            temp_path = temp_file.name
        
        # Extract text using OCR
        extracted_text = OCRService.extract_text(temp_path, file_type)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if extracted_text:
            # Update document with extracted text
            documents_collection.update_one(
                {"document_id": document_id},
                {
                    "$set": {
                        "extracted_text": extracted_text,
                        "processed": True
                    }
                }
            )
            
            # Add to vector store for RAG
            ContextBuilderService.add_document(
                document_id=document_id,
                text=extracted_text,
                metadata={
                    "document_id": document_id,
                    "user_id": user_id,
                    "filename": filename,
                    "file_type": file_type
                }
            )
            
            print(f"Successfully processed document {document_id}")
        else:
            print(f"No text extracted from document {document_id}")
            
    except Exception as e:
        print(f"Error processing document {document_id}: {e}")

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user)
):
    """Upload a medical document (will be processed with OCR)"""
    documents_collection = get_documents_collection()
    
    # Save file to GridFS
    file_info = await StorageService.save_file(file, current_user["user_id"])
    
    # Generate document ID
    document_id = f"D{str(uuid.uuid4().hex[:8]).upper()}"
    
    # Create document record
    document_doc = {
        "document_id": document_id,
        "user_id": current_user["user_id"],
        "file_id": file_info["file_id"],
        "filename": file_info["filename"],
        "file_type": file_info["file_type"],
        "file_size": file_info["file_size"],
        "description": description,
        "extracted_text": None,
        "embedding": None,
        "processed": False,
        "uploaded_at": datetime.now()
    }
    
    documents_collection.insert_one(document_doc)
    document_doc.pop('_id')
    
    # Start OCR processing in background
    background_tasks.add_task(
        process_document_ocr,
        document_id=document_id,
        file_id=file_info["file_id"],
        filename=file_info["filename"],
        file_type=file_info["file_type"],
        user_id=current_user["user_id"]
    )
    
    return DocumentResponse(**document_doc)

@router.get("/", response_model=List[DocumentResponse])
async def get_my_documents(current_user: UserResponse = Depends(get_current_user)):
    """Get all documents for current user"""
    documents_collection = get_documents_collection()
    documents = list(documents_collection.find({"user_id": current_user["user_id"]}).sort("uploaded_at", -1))
    
    if not documents:
        return []
    
    for doc in documents:
        doc.pop('_id')
    
    return [DocumentResponse(**doc) for doc in documents]

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get document by ID"""
    documents_collection = get_documents_collection()
    document = documents_collection.find_one({
        "document_id": document_id,
        "user_id": current_user["user_id"]
    })
    
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
    document = documents_collection.find_one({
        "document_id": document_id,
        "user_id": current_user["user_id"]
    })

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )

    file = StorageService.get_file(document["file_id"])
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return StreamingResponse(
        file, 
        media_type=file.content_type, 
        headers={"Content-Disposition": f"attachment; filename={file.filename}"}
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Delete document"""
    documents_collection = get_documents_collection()
    
    # Get document
    document = documents_collection.find_one({
        "document_id": document_id,
        "user_id": current_user["user_id"]
    })
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )
    
    # Delete file from storage
    StorageService.delete_file(document["file_id"])
    
    # Delete document record
    documents_collection.delete_one({"document_id": document_id})
    
    return None
