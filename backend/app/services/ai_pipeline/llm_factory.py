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
        else:
            content = "Mock response"
            
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
        # For now, we default to it if import works, assuming user followed instructions.
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
