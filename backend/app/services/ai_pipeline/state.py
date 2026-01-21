from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid

class PlanOption(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    option_number: int
    start_time: str
    end_time: str
    reasoning: str
    impact: Optional[str] = None

class TaskAnalysisState(BaseModel):
    """State for task analysis workflow (Pydantic)."""
    # Inputs
    task_id: str
    title: str
    description: Optional[str] = None
    context_notes: Optional[str] = None
    priority: str = "medium"
    user_id: str
    deadline: Optional[str] = None
    
    # Analysis outputs
    estimated_duration_minutes: Optional[int] = None
    suggested_tags: List[str] = []
    ai_reasoning: Optional[str] = None
    
    # Scheduling data
    calendar_events: List[Dict] = []
    scheduling_options: List[PlanOption] = []
    selected_option_id: Optional[str] = None
    execution_result: Optional[str] = None
    
    # Control flags
    error_message: Optional[str] = None
