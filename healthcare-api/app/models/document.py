from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    document_id: str
    patient_id: str
    file_id: str
    filename: str
    file_type: str
    file_size: int
    description: Optional[str]
    uploaded_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "D12345",
                "patient_id": "P12345",
                "file_id": "60f1b3b3b3b3b3b3b3b3b3b3",
                "filename": "xray_chest.pdf",
                "file_type": "application/pdf",
                "file_size": 1024000,
                "description": "Chest X-Ray Report"
            }
        }