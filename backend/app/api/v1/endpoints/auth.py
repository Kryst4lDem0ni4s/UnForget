from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.core.security import create_access_token
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Mock auth - accept any email/password for MVP
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()
    
    if not user:
        # Create user on first login (MVP) - only use fields that exist in User model
        user = User(email=request.email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    token = create_access_token(subject=str(user.id))
    return LoginResponse(access_token=token)
