
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, date

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    subscription_tier: Optional[str] = "free"
    subscription_status: Optional[str] = "active"

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    auth_provider_id: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass
