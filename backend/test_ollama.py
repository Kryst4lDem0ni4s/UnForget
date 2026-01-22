from app.services.ai_pipeline.llm_factory import get_llm

def test_connection():
    width = 40
    print("-" * width)
    print("Testing Ollama Connection...")
    print("-" * width)
    
    try:
        # 1. Get LLM Instance
        llm = get_llm()
        print(f"LLM Type: {type(llm).__name__}")
        
        # 2. Test Invoke
        print("\nSending prompt: 'Hello, are you ready to plan?'")
        response = llm.invoke("Hello, are you ready to plan? Reply efficiently.")
        
        print("\nResponse Received:")
        print(f"> {response.content}")
        print("-" * width)
        print("✅ SUCCESS: Connected to Ollama")
        
    except Exception as e:
        print("\n❌ FAILED: Could not connect or invoke.")
        print(f"Error: {e}")
        
if __name__ == "__main__":
    test_connection()
