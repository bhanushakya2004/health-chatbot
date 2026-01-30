from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.database import Database
from app.routes import patient, report, document, chat, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Database.connect()
    print("✅ Connected to MongoDB")
    yield
    # Shutdown
    Database.close()
    print("❌ Closed MongoDB connection")

app = FastAPI(
    title="Healthcare Consultant API",
    description="API for managing patient records, medical reports, and AI-powered health consultation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(report.router)
app.include_router(document.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Healthcare Consultant API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "patients": "/patients",
            "reports": "/reports",
            "documents": "/documents",
            "chat": "/healthchat"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run with: uvicorn app.main:app --reload
