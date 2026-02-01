from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from app.models.user import UserCreate, UserResponse, Token, UserUpdate
from app.security import create_access_token, get_password_hash, verify_password
from app.config.database import get_users_collection
from app.dependencies import get_current_user
from app.services.health_report_agent import HealthReportAgent
import uuid

router = APIRouter(tags=["Authentication"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Create a new user.
    """
    users_collection = get_users_collection()
    
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user document
    user_doc = {
        "user_id": f"U{str(uuid.uuid4().hex[:8]).upper()}",
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "created_at": datetime.now(),
        "age": None,
        "gender": None,
        "health_summary": None,
        "medical_conditions": [],
        "last_summary_update": None
    }
    
    users_collection.insert_one(user_doc)
    user_doc.pop("_id")
    user_doc.pop("hashed_password")

    return UserResponse(**user_doc)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user.
    """
    users_collection = get_users_collection()
    user = users_collection.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current user.
    """
    return current_user

@router.put("/users/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    """
    Update current user profile.
    """
    users_collection = get_users_collection()
    
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    
    if update_data:
        users_collection.update_one(
            {"user_id": current_user["user_id"]},
            {"$set": update_data}
        )
    
    updated_user = users_collection.find_one({"user_id": current_user["user_id"]})
    updated_user.pop("_id", None)
    updated_user.pop("hashed_password", None)
    
    return UserResponse(**updated_user)

@router.post("/users/me/health-summary")
async def generate_health_summary(current_user: UserResponse = Depends(get_current_user)):
    """
    Generate comprehensive health summary from user's chat history, documents, and reports.
    """
    try:
        # Generate health summary using AI agent
        result = HealthReportAgent.generate_health_summary(current_user["user_id"])
        
        # Update user document
        users_collection = get_users_collection()
        users_collection.update_one(
            {"user_id": current_user["user_id"]},
            {
                "$set": {
                    "health_summary": result["health_summary"],
                    "medical_conditions": result["medical_conditions"],
                    "last_summary_update": datetime.now()
                }
            }
        )
        
        return {
            "message": "Health summary generated successfully",
            "health_summary": result["health_summary"],
            "medical_conditions": result["medical_conditions"],
            "updated_at": datetime.now()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating health summary: {str(e)}"
        )

@router.get("/users/me/health-summary")
async def get_health_summary(current_user: UserResponse = Depends(get_current_user)):
    """
    Get user's current health summary.
    """
    users_collection = get_users_collection()
    user = users_collection.find_one({"user_id": current_user["user_id"]})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "health_summary": user.get("health_summary"),
        "medical_conditions": user.get("medical_conditions", []),
        "last_updated": user.get("last_summary_update")
    }
