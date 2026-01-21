from typing import Any, Dict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
import os

from app.services.ai_pipeline.state import TaskAnalysisState
from app.services.ai_pipeline.nodes.analyze import analyze_task
from app.services.ai_pipeline.nodes.schedule import schedule_task
from app.services.ai_pipeline.nodes.execute import execute_task

# Defined node for pickle capability
def human_review_node(state: TaskAnalysisState) -> Dict:
    # Placeholder for review step
    return {}

# Build the graph structure
def create_graph_builder(with_human_loop: bool = False):
    workflow = StateGraph(TaskAnalysisState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_task)
    workflow.add_node("schedule", schedule_task)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "schedule")
    
    if with_human_loop:
        workflow.add_node("human_review", human_review_node)
        workflow.add_node("execute", execute_task)
        
        workflow.add_edge("schedule", "human_review")
        workflow.add_edge("human_review", "execute")
        workflow.add_edge("execute", END)
    else:
        workflow.add_edge("schedule", END)
        
    return workflow

# 1. One-Shot Graph (Legacy/Testing) - No persistence, no interrupts matches existing tests
one_shot_workflow = create_graph_builder(with_human_loop=False).compile()

async def process_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy one-shot execution for existing endpoints."""
    # Convert dict keys to match Pydantic if needed, but invoke accepts dicts
    result = await one_shot_workflow.ainvoke(task_data)
    return result

# 2. HITL Graph (Production/Async) - With persistence
_checkpointer = None

async def get_checkpointer():
    global _checkpointer
    if _checkpointer is None:
        db_path = "ai_checkpoints.db"
        conn = await aiosqlite.connect(db_path)
        # Assuming conn stays open. In prod, use connection pool or lifespan manager
        _checkpointer = AsyncSqliteSaver(conn)
        await _checkpointer.setup()
    return _checkpointer

async def get_hitl_app():
    checkpointer = await get_checkpointer()
    workflow = create_graph_builder(with_human_loop=True)
    return workflow.compile(checkpointer=checkpointer, interrupt_before=["human_review"])
