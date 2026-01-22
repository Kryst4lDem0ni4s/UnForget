from typing import Any, List, Optional
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
    # Return scheduling options
    options = result.get("scheduling_options", [])
    
    return SchedulingResponse(
        task_id=str(task.id),
        options=[SchedulingOption(**opt) for opt in options]
    )

# --- Async / HITL Endpoints ---

import uuid
from fastapi import BackgroundTasks
from app.services.ai_pipeline.graph import get_hitl_app

class StartWorkflowResponse(BaseModel):
    thread_id: str

class WorkflowStatusResponse(BaseModel):
    thread_id: str
    status: str  # "processing", "waiting_input", "completed", "error", "not_found"
    options: List[SchedulingOption] = []
    error: Optional[str] = None

class ResumeWorkflowRequest(BaseModel):
    selected_option_id: str

async def run_pipeline_background(initial_state: dict, thread_id: str):
    app = await get_hitl_app()
    config = {"configurable": {"thread_id": thread_id}}
    await app.ainvoke(initial_state, config)

async def run_resume_background(thread_id: str, selected_option_id: str):
    app = await get_hitl_app()
    config = {"configurable": {"thread_id": thread_id}}
    # Resume by proceeding (update state explicitly, then resume)
    await app.aupdate_state(config, {"selected_option_id": selected_option_id})
    await app.ainvoke(None, config)

class AIStartRequest(BaseModel):
    """Request model for starting AI workflow."""
    task_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    task_description: Optional[str] = None  # Frontend compatibility

@router.post("/start", response_model=StartWorkflowResponse)
async def start_workflow(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request: AIStartRequest,
    current_user: models.User = Depends(security.get_current_user),
    background_tasks: BackgroundTasks,
) -> Any:
    """Start async AI workflow. Creates task if not provided."""
    
    task = None
    
    # 1. Try to find existing task if ID provided
    if request.task_id:
        task = await crud.task.get(db=db, id=request.task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if str(task.user_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")
            
    # 2. If no task_id, create a new one from description
    else:
        # Handle 'task_description' alias from frontend
        desc = request.description or request.task_description
        if not request.title and not desc:
             raise HTTPException(status_code=400, detail="Must provide task_id OR title/description")
             
        title = request.title or (desc[:50] + "..." if desc else "New Task")
        
        task_in = schemas.TaskCreate(
            title=title,
            description=desc,
            status="pending",
            priority="medium"
        )
        task = await crud.task.create_with_owner(db=db, obj_in=task_in, owner_id=current_user.id)
    
    # Prepare initial state
    initial_state = {
        "task_id": str(task.id),
        "user_id": str(task.user_id),
        "title": task.title,
        "description": task.description,
        "context_notes": task.context_notes,
        "priority": task.priority or "medium",
        "deadline": task.deadline and task.deadline.isoformat(),
        "calendar_events": [] # TODO: Fetch real events
    }
    
    thread_id = str(uuid.uuid4())
    background_tasks.add_task(run_pipeline_background, initial_state, thread_id)
    
    return {"thread_id": thread_id}

@router.get("/{thread_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    thread_id: str,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """Get status of async workflow."""
    try:
        app = await get_hitl_app()
        config = {"configurable": {"thread_id": thread_id}}
        state_snapshot = await app.aget_state(config)
        
        if not state_snapshot:
             return {"thread_id": thread_id, "status": "not_found"}
             
        state_data = state_snapshot.values
        # Security check
        if state_data.get('user_id') != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")
            
        next_step = state_snapshot.next
        status = "processing"
        
        if not next_step:
            status = "completed"
        elif "human_review" in next_step:
            status = "waiting_input"
        
        options_data = state_data.get("scheduling_options", [])
        # Ensure compatibility with Pydantic list of models
        options = []
        if options_data:
             # state might hold dicts or models depending on how langgraph stored it
             for opt in options_data:
                 if hasattr(opt, 'dict'):
                     options.append(SchedulingOption(**opt.dict()))
                 elif isinstance(opt, dict):
                     options.append(SchedulingOption(**opt))
                 else:
                     # Pydantic model directly
                     options.append(SchedulingOption(
                         option_number=opt.option_number,
                         start_time=opt.start_time,
                         end_time=opt.end_time,
                         reasoning=opt.reasoning,
                         impact=opt.impact
                     ))

        return {
            "thread_id": thread_id,
            "status": status,
            "options": options
        }
    except Exception as e:
        print(f"Error getting status: {e}")
        return {"thread_id": thread_id, "status": "error", "error": str(e)}

@router.post("/{thread_id}/resume")
async def resume_workflow_endpoint(
    *,
    thread_id: str,
    request: ResumeWorkflowRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """Resume workflow with user selection."""
    # Verify auth
    try:
        app = await get_hitl_app()
        config = {"configurable": {"thread_id": thread_id}}
        state_snapshot = await app.aget_state(config)
        if not state_snapshot:
             raise HTTPException(status_code=404, detail="Thread not found")
        if state_snapshot.values.get('user_id') != str(current_user.id):
             raise HTTPException(status_code=403, detail="Not authorized")
             
        background_tasks.add_task(run_resume_background, thread_id, request.selected_option_id)
        return {"status": "resumed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
