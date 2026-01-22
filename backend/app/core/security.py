
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import jwt

from app.api.deps import get_db
from app import crud
from app.core.config import settings

security = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY

def create_access_token(subject: str) -> str:
    """Create JWT token for MVP."""
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# Mock auth for MVP - Replace with Firebase Admin SDK in production
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:

    """
    Validate JWT token and extract user ID.
    In production, validate Firebase token and extract user_id.
    """
    try:
        # Decode JWT token
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),

):
    """
    Get current user from database.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
