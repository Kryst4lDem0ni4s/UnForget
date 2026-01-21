
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EventBase(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_fixed: Optional[bool] = False
    source: Optional[str] = "local"

class EventCreate(EventBase):
    title: str
    start_time: datetime
    end_time: datetime

class EventUpdate(EventBase):
    pass

class EventInDBBase(EventBase):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    task_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass
