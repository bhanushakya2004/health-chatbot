from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "healthcare_db")

class Database:
    client = None
    db = None
    fs = None
    
    @classmethod
    def connect(cls):
        """Initialize database connection"""
        cls.client = MongoClient(MONGODB_URL)
        cls.db = cls.client[DATABASE_NAME]
        cls.fs = GridFS(cls.db)
        return cls.db
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.db is None:
            cls.connect()
        return cls.db

    @classmethod
    def get_fs(cls):
        """Get GridFS instance"""
        if cls.fs is None:
            cls.connect()
        return cls.fs
    
    @classmethod
    def close(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()

# Collections
def get_patients_collection():
    db = Database.get_db()
    return db["patients"]

def get_reports_collection():
    db = Database.get_db()
    return db["reports"]

def get_documents_collection():
    db = Database.get_db()
    return db["documents"]

def get_users_collection():
    db = Database.get_db()
    return db["users"]

def get_chats_collection():
	db = Database.get_db()
	return db["chats"]