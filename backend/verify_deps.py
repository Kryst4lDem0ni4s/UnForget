try:
    import langgraph
    print(f"LangGraph version: {langgraph.__version__ if hasattr(langgraph, '__version__') else 'unknown'}")
    print(f"LangGraph file: {langgraph.__file__}")
except ImportError as e:
    print(f"ImportError: {e}")

try:
    import langchain_openai
    print("LangChain OpenAI found")
except ImportError:
    print("LangChain OpenAI NOT found")
