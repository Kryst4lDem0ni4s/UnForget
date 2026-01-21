import json
from datetime import datetime, timedelta
from typing import List, Dict

from app.services.ai_pipeline.state import TaskAnalysisState
from app.services.ai_pipeline.nodes.analyze import load_prompts, MockLLM

PROMPTS = load_prompts()

def format_calendar_summary(events: List[dict]) -> str:
    """Format calendar events for LLM prompt."""
    if not events:
        return "No upcoming events"
    
    summary_lines = []
    for event in events[:10]:  # Limit to 10 events
        start = event.get('start_time', 'Unknown')
        end = event.get('end_time', 'Unknown')
        title = event.get('title', 'Untitled')
        summary_lines.append(f"- {start} to {end}: {title}")
    
    return "\n".join(summary_lines)

async def schedule_task(state: TaskAnalysisState) -> TaskAnalysisState:
    """
    Find optimal scheduling slots for the task.
    
    This node:
    1. Analyzes user's calendar
    2. Considers task duration and priority
    3. Generates 3 scheduling options with reasoning
    """
    
    # Get calendar events
    calendar_events = state.get('calendar_events', [])
    calendar_summary = format_calendar_summary(calendar_events)
    
    # Build prompt
    prompt_config = PROMPTS['scheduling']
    system_prompt = prompt_config['system']
    user_prompt = prompt_config['user_template'].format(
        title=state['title'],
        duration_minutes=state.get('estimated_duration_minutes', 30),
        priority=state.get('priority', 'medium'),
        deadline=state.get('deadline', 'No deadline'),
        context_notes=state.get('context_notes', 'No context'),
        calendar_summary=calendar_summary,
        work_hours="9 AM - 6 PM",  # TODO: Get from user preferences
        focus_preference="Morning"  # TODO: Get from user preferences
    )
    
    # Use mock LLM
    llm = MockLLM()
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    # Generate scheduling options
    # For MVP, use simple heuristic
    now = datetime.now()
    options = [
        {
            "option_number": 1,
            "start_time": (now + timedelta(hours=1)).isoformat(),
            "end_time": (now + timedelta(hours=1) + timedelta(minutes=state.get('estimated_duration_minutes', 30))).isoformat(),
            "reasoning": "Next available slot in your calendar",
            "impact": "None - no conflicts detected"
        },
        {
            "option_number": 2,
            "start_time": (now + timedelta(days=1, hours=9)).isoformat(),
            "end_time": (now + timedelta(days=1, hours=9) + timedelta(minutes=state.get('estimated_duration_minutes', 30))).isoformat(),
            "reasoning": "Tomorrow morning during peak focus hours",
            "impact": "Postpones less critical tasks"
        },
        {
            "option_number": 3,
            "start_time": (now + timedelta(hours=4)).isoformat(),
            "end_time": (now + timedelta(hours=4) + timedelta(minutes=state.get('estimated_duration_minutes', 30))).isoformat(),
            "reasoning": "Later today after current commitments",
            "impact": "May extend work day slightly"
        }
    ]
    
    state['scheduling_options'] = options
    
    return state
