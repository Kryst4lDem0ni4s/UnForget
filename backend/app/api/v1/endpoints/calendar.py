from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from app.models.task import Task
from app.schemas.task import Task as TaskSchema

router = APIRouter()

@router.get("/events", response_model=List[Any])
def get_calendar_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve tasks that have a deadline, formatted as calendar events.
    """
    # For MVP, we treat tasks with deadlines as events.
    # In future, we can have a separate 'Event' model.
    tasks = db.query(Task).filter(Task.deadline != None).offset(skip).limit(limit).all()
    
    events = []
    for task in tasks:
        events.append({
            "id": str(task.id),
            "title": task.title,
            "start": task.deadline, # Assuming deadline is the start time for simple tasks
            "end": task.deadline,   # Duration 0 for point-in-time tasks
            "type": "task_deadline",
            "priority": task.priority
        })
        
    return events
