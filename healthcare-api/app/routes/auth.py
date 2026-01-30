from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import UserCreate, UserResponse, Token, UserUpdate
from app.security import create_access_token, get_password_hash, verify_password
from app.config.database import get_users_collection
from app.dependencies import get_current_user
import uuid
from datetime import datetime

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
    Update current user.
    """
    users_collection = get_users_collection()
    
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    
    if update_data:
        users_collection.update_one(
            {"user_id": current_user["user_id"]},
            {"$set": update_data}
        )
    
    updated_user = users_collection.find_one({"user_id": current_user["user_id"]})
    
    return UserResponse(**updated_user)
