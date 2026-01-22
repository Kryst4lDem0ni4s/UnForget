import os
import json
from typing import Any, Optional

class MockLLM:
    """Mock LLM for testing without API keys."""
    def invoke(self, prompt: str) -> Any:
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        # Simple heuristic-based response
        if "estimated duration" in str(prompt).lower():
            content = json.dumps({
                "estimated_duration_minutes": 60,
                "suggested_tags": ["work", "analysis"],
                "reasoning": "Based on task complexity, estimated 60 minutes (Mock Analysis)"
            })
        elif "scheduling options" in str(prompt).lower() or "scheduler" in str(prompt).lower():
             content = json.dumps({
                "options": [
                    {
                        "option_number": 1,
                        "start_time": "2026-01-22T10:00:00",
                        "end_time": "2026-01-22T11:00:00",
                        "reasoning": "Next available slot",
                        "impact": "None"
                    },
                    {
                        "option_number": 2,
                        "start_time": "2026-01-23T09:00:00",
                        "end_time": "2026-01-23T10:00:00",
                        "reasoning": "Morning focus time",
                        "impact": "None"
                    },
                    {
                        "option_number": 3,
                        "start_time": "2026-01-23T14:00:00",
                        "end_time": "2026-01-23T15:00:00",
                        "reasoning": "Afternoon slot",
                        "impact": "None"
                    }
                ]
            })
        else:
            content = json.dumps({"reasoning": "Mock response"})
            
        return MockResponse(content)

def get_llm(temperature: float = 0):
    """
    Get the LLM instance based on configuration.
    Prioritizes Ollama (local) logic.
    """
    try:
        from langchain_community.chat_models import ChatOllama
        
        # User confirmed Ollama is served.
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        # Detected 'deepseek-r1:7b' via `ollama list`
        model = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
        
        print(f"Connecting to Ollama at {base_url} with model {model}...")
        
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature
        )
        return llm
    except ImportError:
        print("langchain_community not installed. Falling back to Mock.")
    except Exception as e:
        print(f"Ollama init failed: {e}")

    # Fallback to MockLLM
    print("Using MockLLM (Ollama connection failed or library missing)")
    return MockLLM()
