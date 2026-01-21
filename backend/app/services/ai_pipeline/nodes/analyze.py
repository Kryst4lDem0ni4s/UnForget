import os
import yaml
import json
from typing import Dict, Any
from pathlib import Path

from app.services.ai_pipeline.state import TaskAnalysisState

# Mock LLM for MVP - Replace with real LangChain LLM
class MockLLM:
    """Mock LLM for testing without API keys."""
    
    def invoke(self, prompt: str) -> str:
        # Simple heuristic-based response
        if "estimated duration" in prompt.lower():
            return json.dumps({
                "estimated_duration_minutes": 60,
                "suggested_tags": ["work", "analysis"],
                "reasoning": "Based on task complexity, estimated 60 minutes"
            })
        return "Mock response"

# Load prompts
def load_prompts() -> Dict[str, Any]:
    """Load prompt templates from YAML."""
    # Go up one level from nodes/ to ai_ pipeline/ then to prompts/
    prompt_file = Path(__file__).parent.parent / "prompts" / "templates.yaml"
    with open(prompt_file, 'r') as f:
        return yaml.safe_load(f)

PROMPTS = load_prompts()

async def analyze_task(state: TaskAnalysisState) -> TaskAnalysisState:
    """
    Analyze task and estimate duration.
    
    This node:
    1. Takes task details
    2. Uses LLM to estimate duration
    3. Suggests tags
    4. Provides reasoning
    """
    
    # Build prompt from template
    prompt_config = PROMPTS['task_analysis']
    system_prompt = prompt_config['system']
    user_prompt = prompt_config['user_template'].format(
        title=state['title'],
        description=state.get('description', 'No description'),
        context_notes=state.get('context_notes', 'No context'),
        priority=state.get('priority', 'medium')
    )
    
    # Use mock LLM for MVP
    # TODO: Replace with actual LangChain LLM (OpenAI/Gemini)
    # from langchain_openai import ChatOpenAI
    # llm = ChatOpenAI(model="gpt-4")
    
    llm = MockLLM()
    
    # Invoke LLM
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = llm.invoke(full_prompt)
    
    # Parse response (assuming JSON format)
    try:
        result = json.loads(response)
        state['estimated_duration_minutes'] = result.get('estimated_duration_minutes', 30)
        state['suggested_tags'] = result.get('suggested_tags', [])
        state['ai_reasoning'] = result.get('reasoning', 'AI analysis completed')
    except json.JSONDecodeError:
        # Fallback if response isn't JSON
        state['estimated_duration_minutes'] = 30
        state['ai_reasoning'] = "Default estimate based on task complexity"
    
    return state
