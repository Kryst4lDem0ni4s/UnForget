import asyncio
import os
import sys
from pprint import pprint

# Ensure app in path
sys.path.append(os.getcwd())

from app.services.ai_pipeline.graph import create_graph_builder
from app.services.ai_pipeline.state import TaskAnalysisState
from langgraph.checkpoint.memory import MemorySaver

async def test_logic_flow():
    print("--- Starting AI Logic Stress Test (No Server) ---")
    
    # Setup - Use MemorySaver for logic test to avoid SQLite file locks/management
    memory_checkpointer = MemorySaver()
    
    # 1. Create Graph
    print("1. Building HITL Graph...")
    builder = create_graph_builder(with_human_loop=True)
    app = builder.compile(checkpointer=memory_checkpointer, interrupt_after=["schedule"])
    
    # 2. Start Workflow
    # Use a fixed thread ID
    thread_id = "stress-test-thread-1"
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "task_id": "test-task-1",
        "title": "Stress Test Logic",
        "user_id": "user-1",
        "description": "Testing the backend without server",
        "priority": "high",
        "context_notes": "Urgent verification"
    }
    
    print(f"2. Invoking Start (Thread: {thread_id})...")
    # This should run 'analyze' -> 'schedule' -> and STOP before 'human_review'
    # ainvoke returns the final state (which is the state at interruption)
    result = await app.ainvoke(initial_state, config)
    
    # 3. Verify State at Interrupt
    print("3. Checking Snapshot at Interrupt...")
    snapshot = await app.aget_state(config)
    state = snapshot.values # This should be a Dict or Pydantic model depending on LangGraph version
    next_step = snapshot.next
    
    print(f"   Next Step: {next_step}")
    
    # Check if state is Pydantic object or dict
    if hasattr(state, 'estimated_duration_minutes'):
        duration = state.estimated_duration_minutes
        options = state.scheduling_options
    else:
        duration = state.get('estimated_duration_minutes')
        options = state.get('scheduling_options', [])
    
    print(f"   Estimated Duration: {duration}")
    print(f"   Options Generated: {len(options)}")
    
    if "human_review" not in next_step:
        print("❌ FAILED: Did not pause at human_review")
        print(f"Actual Next: {next_step}")
        return
        
    if not options:
         print("❌ FAILED: No options generated")
         return

    print("✅ Initial Phase Passed. State persisted.")

    # 4. Resume Workflow
    print("4. Resuming with Selection...")
    # Explicitly update state first
    # Select option 1 (which matches option_number=1 in fallback logic)
    await app.aupdate_state(config, {"selected_option_id": "1"})
    
    # Then invoke with None to resume (empty input)
    final_output = await app.ainvoke(None, config)
    
    # 5. Verify Completion
    snapshot = await app.aget_state(config)
    if snapshot.next:
         print(f"❌ FAILED: Workflow did not finish. Next: {snapshot.next}")
    else:
         print("✅ PASSED: Workflow completed successfully.")
         # Check final state
         final_values = snapshot.values
         sel = final_values.get('selected_option_id') if hasattr(final_values, 'get') else getattr(final_values, 'selected_option_id', None)
         print(f"   Selected Option: {sel}")
         
         exec_res = final_values.get('execution_result') if hasattr(final_values, 'get') else getattr(final_values, 'execution_result', None)
         print(f"   Execution Result: {exec_res}")
         
         if not exec_res or "Confirmed" not in exec_res:
             print("❌ FAILED: Execution result missing or incorrect")

if __name__ == "__main__":
    asyncio.run(test_logic_flow())
