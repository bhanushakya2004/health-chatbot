from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security import decode_access_token
from app.models.user import TokenData
from app.config.database import get_users_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    token_data = TokenData(email=email)
    
    users_collection = get_users_collection()
    user = users_collection.find_one({"email": token_data.email})
    
    if user is None:
        raise credentials_exception
    return user
