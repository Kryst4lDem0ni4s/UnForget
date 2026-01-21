from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.services.ai_pipeline.graph import process_task

router = APIRouter()

class AIAnalysisRequest(BaseModel):
    """Request model for AI task analysis."""
    task_id: str

class AIAnalysisResponse(BaseModel):
    """Response model for AI task analysis."""
    task_id: str
    estimated_duration_minutes: int
    suggested_tags: List[str]
    ai_reasoning: str

class SchedulingRequest(BaseModel):
    """Request Model for AI scheduling."""
    task_id: str

class SchedulingOption(BaseModel):
    """Single scheduling option."""
    option_number: int
    start_time: str
    end_time: str
    reasoning: str
    impact: str

class SchedulingResponse(BaseModel):
    """Response model for AI scheduling."""
    task_id: str
    options: List[SchedulingOption]

@router.post("/analyze-task", response_model=AIAnalysisResponse)
async def analyze_task_endpoint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request: AIAnalysisRequest,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Analyze a task using AI to estimate duration and categorize.
    """
    # Get task from database
    task = await crud.task.get(db=db, id=request.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if str(task.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Prepare task data for AI pipeline
    task_data = {
        "task_id": str(task.id),
        "user_id": str(task.user_id),
        "title": task.title,
        "description": task.description,
        "context_notes": task.context_notes,
        "priority": task.priority or "medium",
        "deadline": task.deadline
    }
    
    # Process through AI pipeline
    result = await process_task(task_data)
    
    # Update task with AI results
    update_data = {
        "estimated_duration_minutes": result.get("estimated_duration_minutes"),
        "ai_reasoning": result.get("ai_reasoning")
    }
    await crud.task.update(db=db, db_obj=task, obj_in=update_data)
    
    return AIAnalysisResponse(
        task_id=str(task.id),
        estimated_duration_minutes=result.get("estimated_duration_minutes", 30),
        suggested_tags=result.get("suggested_tags", []),
        ai_reasoning=result.get("ai_reasoning", "")
    )

@router.post("/schedule", response_model=SchedulingResponse)
async def schedule_task_endpoint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request: SchedulingRequest,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Get AI-generated scheduling options for a task.
    """
    # Get task from database
    task = await crud.task.get(db=db, id=request.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if str(task.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get user's calendar events
    # TODO: Fetch from calendar_events table
    calendar_events = []
    
    # Prepare task data
    task_data = {
        "task_id": str(task.id),
        "user_id": str(task.user_id),
        "title": task.title,
        "description": task.description,
        "context_notes": task.context_notes,
        "priority": task.priority or "medium",
        "estimated_duration_minutes": task.estimated_duration_minutes or 30,
        "deadline": task.deadline,
        "calendar_events": calendar_events
    }
    
    # Process through AI pipeline
    result = await process_task(task_data)
    
    # Return scheduling options
    options = result.get("scheduling_options", [])
    
    return SchedulingResponse(
        task_id=str(task.id),
        options=[SchedulingOption(**opt) for opt in options]
    )
