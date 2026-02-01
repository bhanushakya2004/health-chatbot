from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from app.config.database import Database
from app.routes import report, document, chat, auth
from app.utils.logging_middleware import LoggingMiddleware
from app.utils.logger import info, error
from app.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        Database.connect()
        info("🚀 Application started - MongoDB connected")
    except Exception as e:
        error("Failed to connect to MongoDB", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    try:
        Database.close()
        info("🛑 Application shutdown - MongoDB connection closed")
    except Exception as e:
        error("Error during shutdown", exc_info=True)

app = FastAPI(
    title="Healthcare Consultant API",
    description="API for managing medical reports, documents, and AI-powered health consultation",
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

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(auth.router)
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
            "auth": "/login, /signup",
            "reports": "/reports",
            "documents": "/documents",
            "chat": "/chats"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run with: uvicorn app.main:app --reload
