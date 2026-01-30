from fastapi import UploadFile
from app.config.database import Database
from bson.objectid import ObjectId

class StorageService:
    
    @staticmethod
    async def save_file(file: UploadFile, patient_id: str) -> dict:
        """Save uploaded file to GridFS and return file info"""
        fs = Database.get_fs()
        
        # Save file to GridFS
        file_id = fs.put(file.file, filename=file.filename, content_type=file.content_type, patient_id=patient_id)
        
        # Get file info
        file_info = fs.get(file_id)
        
        return {
            "file_id": str(file_id),
            "filename": file_info.filename,
            "file_type": file_info.content_type,
            "file_size": file_info.length,
        }
    
    @staticmethod
    def delete_file(file_id: str):
        """Delete a file from GridFS"""
        fs = Database.get_fs()
        fs.delete(ObjectId(file_id))

    @staticmethod
    def get_file(file_id: str):
        """Get a file from GridFS"""
        fs = Database.get_fs()
        try:
            return fs.get(ObjectId(file_id))
        except Exception:
            return None