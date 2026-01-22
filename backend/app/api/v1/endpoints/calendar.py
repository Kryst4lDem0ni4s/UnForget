from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from app.api import deps
from app.models.task import Task
from app.schemas.task import Task as TaskSchema

router = APIRouter()

@router.get("/events", response_model=List[Any])
async def get_calendar_events(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve tasks that have a deadline, formatted as calendar events.
    """
    from sqlalchemy import select
    
    # Use standard select query
    query = select(Task).where(Task.deadline != None).offset(skip).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    events = []
    for task in tasks:
        events.append({
            "id": str(task.id),
            "title": task.title,
            "start": task.deadline,
            "end": task.deadline,   # Duration 0 for point-in-time tasks
            "type": "task_deadline",
            "priority": task.priority
        })
        
    return events
