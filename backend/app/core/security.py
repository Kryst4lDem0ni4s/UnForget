
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_db
from app import crud

# Simple bearer token security for MVP
security = HTTPBearer()

# Mock auth for MVP - Replace with Firebase Admin SDK in production
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:

    """
    Mock authentication - returns a hardcoded user ID.
    In production, validate Firebase token and extract user_id.
    """
    # TODO: Implement Firebase Admin token verification
    # decoded_token = auth.verify_id_token(credentials.credentials)
    # user_id = decoded_token['uid']
    
    # For MVP, we'll accept any token and return a test user ID
    # You can pass "test-user" as bearer token
    if credentials.credentials == "test-user":
        # Return a fixed UUID for testing
        return "00000000-0000-0000-0000-000000000001"

    
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
