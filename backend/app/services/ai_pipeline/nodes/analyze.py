import json
from typing import Dict, Any, cast
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

async def analyze_task(state: TaskAnalysisState) -> dict:
    """
    Analyze task and estimate duration using LLM.
    """
    prompt_config = PROMPTS['task_analysis']
    system_prompt = prompt_config['system']
    user_prompt = prompt_config['user_template'].format(
        title=state.title,
        description=state.description or 'No description',
        context_notes=state.context_notes or 'No context',
        priority=state.priority
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
        # Fallback if invoke fails (e.g. Ollama connection refused)
        print(f"LLM Invoke failed: {e}. Falling back to Mock.")
        from app.services.ai_pipeline.llm_factory import MockLLM
        llm = MockLLM()
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = llm.invoke(full_prompt)
        content = response.content
    
    # Clean up content (remove markdown fences if present)
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
        return {
            "estimated_duration_minutes": result.get('estimated_duration_minutes', 30),
            "suggested_tags": result.get('suggested_tags', []),
            "ai_reasoning": result.get('reasoning', 'AI analysis completed')
        }
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}. Content: {content}")
        return {
            "estimated_duration_minutes": 30,
            "ai_reasoning": f"Error parsing AI response: {str(e)}"
        }
