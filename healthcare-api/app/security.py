import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_BCRYPT = True
except Exception:
    USE_BCRYPT = False

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    """Verify password with bcrypt or fallback"""
    # Check if it's a fallback hash
    if hashed_password.startswith("$fallback$"):
        fallback_hash = "$fallback$" + hashlib.sha256(plain_password.encode()).hexdigest()
        return fallback_hash == hashed_password
    
    # Try bcrypt
    if USE_BCRYPT:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    return False

def get_password_hash(password):
    """Hash password with bcrypt or fallback"""
    if USE_BCRYPT:
        try:
            return pwd_context.hash(password)
        except Exception:
            return "$fallback$" + hashlib.sha256(password.encode()).hexdigest()
    else:
        return "$fallback$" + hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
