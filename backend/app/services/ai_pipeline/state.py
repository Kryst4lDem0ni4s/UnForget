from typing import TypedDict, List, Optional
from datetime import datetime

class TaskAnalysisState(TypedDict):
    """State for task analysis workflow."""
    task_id: str
    title: str
    description: Optional[str]
    context_notes: Optional[str]
    priority: str
    
    # Outputs from analysis
    estimated_duration_minutes: Optional[int]
    suggested_tags: Optional[List[str]]
    ai_reasoning: Optional[str]
    
    # For scheduling
    calendar_events: Optional[List[dict]]
    scheduling_options: Optional[List[dict]]
    
    # Metadata
    user_id: str
    deadline: Optional[datetime]
