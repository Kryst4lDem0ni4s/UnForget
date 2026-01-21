from app.services.ai_pipeline.state import TaskAnalysisState
from app.services.ai_pipeline.tools import commit_event

async def execute_task(state: TaskAnalysisState) -> dict:
    """
    Execute the selected option using tools.
    """
    selected_id = state.selected_option_id
    if not selected_id:
        return {"error_message": "No option selected for execution"}
    
    # Find the option
    selected_option = None
    options = state.scheduling_options
    
    for opt in options:
        # Handle Pydantic or Dict
        opt_id = getattr(opt, 'id', None)
        if hasattr(opt, 'get'):
             opt_id = opt.get('id')
             
        if str(opt_id) == str(selected_id):
            selected_option = opt
            break
            
    # Fallback to option_number match if ID not found (for testing/simplicity)
    if not selected_option:
        try:
             sel_num = int(selected_id)
             for opt in options:
                 opt_num = getattr(opt, 'option_number', 0)
                 if hasattr(opt, 'get'):
                     opt_num = opt.get('option_number')
                 if opt_num == sel_num:
                     selected_option = opt
                     break
        except:
            pass

    if not selected_option:
        return {"execution_result": "Failed: Option not found"}
        
    # Prepare params
    title = state.title
    start = getattr(selected_option, 'start_time', '') or selected_option.get('start_time')
    end = getattr(selected_option, 'end_time', '') or selected_option.get('end_time')
    
    # Call Tool
    # We invoke the tool directly (deterministic execution)
    result = commit_event.invoke({
        "title": title,
        "start_time": start,
        "end_time": end,
        "description": f"Booked via AI Planner for {state.user_id}"
    })
    
    return {"execution_result": result}
