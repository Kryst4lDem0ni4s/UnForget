
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "pending"
    context_notes: Optional[str] = None

class TaskCreate(TaskBase):
    title: str

class TaskUpdate(TaskBase):
    pass

class TaskInDBBase(TaskBase):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    points_value: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None
    ai_reasoning: Optional[str] = None
    parent_task_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    pass
