import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path
import yaml

from app.services.ai_pipeline.state import TaskAnalysisState
from app.services.ai_pipeline.llm_factory import get_llm

def load_prompts() -> Dict[str, Any]:
    """Load prompt templates from YAML."""
    prompt_file = Path(__file__).parent.parent / "prompts" / "templates.yaml"
    with open(prompt_file, 'r') as f:
        return yaml.safe_load(f)

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

async def schedule_task(state: TaskAnalysisState) -> dict:
    """
    Find optimal scheduling slots for the task using LLM.
    """
    
    # Get calendar events
    calendar_events = state.calendar_events
    calendar_summary = format_calendar_summary(calendar_events)
    
    # Build prompt
    prompt_config = PROMPTS['scheduling']
    system_prompt = prompt_config['system']
    user_prompt = prompt_config['user_template'].format(
        title=state.title,
        duration_minutes=state.estimated_duration_minutes or 30,
        priority=state.priority,
        deadline=state.deadline or 'No deadline',
        context_notes=state.context_notes or 'No context',
        calendar_summary=calendar_summary,
        work_hours="9 AM - 6 PM", 
        focus_preference="Morning"
    )
    
    # Get LLM (Ollama or Mock)
    llm = get_llm(temperature=0)
    
    # Invoke
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response = llm.invoke(messages)
        content = response.content
    except Exception as e:
        print(f"LLM Invoke failed: {e}. Falling back to Mock.")
        from app.services.ai_pipeline.llm_factory import MockLLM
        llm = MockLLM()
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = llm.invoke(full_prompt)
        content = response.content
    
    # Clean up content
    content = str(content).strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    # Parse JSON
    try:
        result = json.loads(content)
        options = result.get('options', [])
        # Ensure we have valid structure if LLM hallucinates
        if not options:
             raise ValueError("No options returned")
             
        return {"scheduling_options": options}
        
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON Error in scheduling: {e}. Content: {content}")
        # Fallback to current time
        now = datetime.now()
        fallback_option = {
            "option_number": 1,
            "start_time": (now + timedelta(hours=1)).isoformat(),
            "end_time": (now + timedelta(hours=2)).isoformat(),
            "reasoning": f"Fallback: Error parsing AI ({str(e)})",
            "impact": "Unknown"
        }
        return {"scheduling_options": [fallback_option]}
