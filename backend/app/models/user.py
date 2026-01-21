
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, Enum, ForeignKey
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, Enum, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    email = Column(String, unique=True, nullable=False)
    auth_provider_id = Column(String)
    subscription_tier = Column(String, default="free")
    subscription_status = Column(String, default="active")
    tasks_used_this_month = Column(Integer, default=0)
    billing_period_start = Column(Date, default=func.current_date())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship("Task", back_populates="user")
    events = relationship("CalendarEvent", back_populates="user")
    integrations = relationship("UserIntegration", back_populates="user")

class UserIntegration(Base):
    __tablename__ = "user_integrations"

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    provider = Column(String, primary_key=True)
    access_token = Column(String) # Encrypted
    refresh_token = Column(String) # Encrypted
    expires_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="integrations")
