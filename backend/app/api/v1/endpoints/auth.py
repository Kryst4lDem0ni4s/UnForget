from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Mock auth - accept any email/password for MVP
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Create user on first login (MVP)
        user = User(email=request.email, full_name="Test User")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    token = create_access_token(subject=user.id)
    return LoginResponse(access_token=token)
