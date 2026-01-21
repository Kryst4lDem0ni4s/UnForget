from typing import Any, Dict
from langgraph.graph import StateGraph, END

from app.services.ai_pipeline.state import TaskAnalysisState
from app.services.ai_pipeline.nodes.analyze import analyze_task
from app.services.ai_pipeline.nodes.schedule import schedule_task

def create_task_workflow() -> StateGraph:
    """
    Create the LangGraph workflow for task processing.
    
    Workflow:
    1. analyze_task: Estimate duration and categorize
    2. schedule_task: Find optimal time slots
    """
    
    workflow = StateGraph(TaskAnalysisState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_task)
    workflow.add_node("schedule", schedule_task)
    
    # Define edges
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "schedule")
    workflow.add_edge("schedule", END)
    
    return workflow.compile()

# Create the compiled graph
task_workflow = create_task_workflow()

async def process_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a task through the AI pipeline.
    
    Args:
        task_data: Dictionary containing task information
        
    Returns:
        Updated task data with AI analysis and scheduling options
    """
    
    # Invoke the workflow
    result = await task_workflow.ainvoke(task_data)
    
    return result
