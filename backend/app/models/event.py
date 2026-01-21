
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey

from sqlalchemy.orm import relationship
from app.db.base import Base

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    task_id = Column(String, ForeignKey("tasks.id", ondelete="SET NULL"))

    title = Column(String)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    is_fixed = Column(Boolean, default=False)
    source = Column(String)

    user = relationship("User", back_populates="events")
    task = relationship("Task", back_populates="events")
