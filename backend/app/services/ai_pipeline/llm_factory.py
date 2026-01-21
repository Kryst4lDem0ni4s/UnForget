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
    Prioritizes Ollama (local) logic if available.
    """
    # 1. Try Ollama (MVP Goal)
    try:
        from langchain_community.chat_models import ChatOllama
        # Check if we should use Ollama (e.g. by checking if it's reachable or just default)
        
        # Check if Ollama is actually reachable (quick check not implemented here to avoid lag, assumming try/catch invoke works)
        # But we can assume if the module imports, we try it. 
        # Ideally we'd ping localhost:11434 but let's trust the user or failback on runtime error if feasible, 
        # or simplified:
        
        # Only use Ollama if env var is set or we want to force it. 
        # For now, let's look for an explicit flag or default to Mock to avoid "Connection refused" errors slowing down dev 
        # unless user explicitly asked for Ollama testing. 
        
        # User asked: "testing the ollama based functionality"
        # So we SHOULD try Ollama.
        
        llm = ChatOllama(
            model="llama3",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=temperature
        )
        return llm
    except ImportError:
        pass
    except Exception as e:
        print(f"Ollama init failed: {e}")

    # 2. Fallback to MockLLM
    print("Using MockLLM (Ollama not found or configured)")
    return MockLLM()
