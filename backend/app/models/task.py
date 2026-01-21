
import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(DateTime(timezone=True))
    priority = Column(String)
    status = Column(String, default="pending")
    points_value = Column(Integer, default=10)
    context_notes = Column(Text)
    estimated_duration_minutes = Column(Integer)
    ai_reasoning = Column(Text)
    parent_task_id = Column(String, ForeignKey("tasks.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")
    subtasks = relationship("Task", remote_side=[id])
    events = relationship("CalendarEvent", back_populates="task")
