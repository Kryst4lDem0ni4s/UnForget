# AI Planner - Optimized AI Architecture & Workflow Plan

## 1. Executive Summary

This document outlines the architectural blueprint for the optimized AI workflow within the AI Planner project. It transitions from the current linear, mock-based implementation to a robust, agentic, and event-driven architecture using **LangGraph** orchestration, **LangComponents**, and **Model Context Protocol (MCP)** principles for tool interoperability.

The core goal is to enable an intelligent "Task to Calendar" pipeline that is resilient, interactive (Human-in-the-loop), and scalable.

## 2. High-Level Architecture

The system follows a **Hub-and-Spoke** agentic pattern where a central Orchestrator (Main Graph) coordinates specialized sub-agents/nodes.

```mermaid
graph TD
    UserRequest --> API[FastAPI Endpoint]
    API --> Orchestrator[LangGraph Orchestrator]
    Orchestrator --> State[Shared State (Redis/Memory)]
    
    subgraph "AI Pipeline (LangGraph)"
        Orchestrator --> Analyzer[Node: Task Analyzer]
        Orchestrator --> ContextGatherer[Node: Context Gatherer]
        Orchestrator --> Scheduler[Node: Schedule Optimizer]
        Orchestrator --> Reviewer[Node: Human Review / HITL]
        Orchestrator --> Executor[Node: Calendar Executor]
    end
    
    subgraph "Tools (MCP Layer)"
        Scheduler --> Tool_CalRead[Calendar Read Tool]
        Executor --> Tool_CalWrite[Calendar Write Tool]
        Analyzer --> Tool_History[History Lookup]
    end
    
    Executor --> External[Google/Outlook API]
```

## 3. Orchestration (LangGraph)

We will upgrade the current simple `analyze -> schedule` linear graph to a stateful, cyclic graph that supports retries and human feedback.

### 3.1. Workflows
1.  **Drafting Phase**: `Input` -> `Analyze` -> `Context` -> `Draft Schedule`
2.  **Review Phase**: `Draft Schedule` -> `Wait for User`
    - *Approve* -> `Execute`
    - *Reject/Refine* -> `Reschedule` (Loop back to Draft)

### 3.2. State Management (`GraphState`)
Instead of a simple `TypedDict`, we will use a Pydantic-validated state to ensure type safety across nodes.

```python
class AgentState(TypedDict):
    # Input
    task_input: TaskInputSchema
    user_preferences: UserPreferences
    
    # Context
    calendar_context: List[Event]
    current_time: datetime
    
    # Working Memory
    analysis_result: TaskAnalysis
    schedule_options: List[ScheduleOption]
    reasoning_logs: List[str]
    
    # Flow Control
    retry_count: int
    error_message: Optional[str]
    human_feedback: Optional[str]
```

## 4. Agents & Nodes Specification

### 4.1. Task Analyzer Node (`analyze`)
-   **Role**: Enriches raw user input into structured metadata.
-   **Tools**: None (Pure LLM).
-   **Input**: Raw text (e.g., "Do taxes").
-   **Output**: Structured Data (Duration: 60m, Priority: High, Tags: [Finance], Subtasks: [...]).
-   **Model**: Low-latency model (e.g., Gemini Flash / GPT-4o-mini).

### 4.2. Context Gatherer Node (`context`)
-   **Role**: Fetches relevant external state required for decision making.
-   **Tools**:
    -   `get_calendar_events(start, end)`: Fetches user's busy slots.
    -   `get_user_preferences()`: Fetches work hours, focus times.
-   **Optimization**: Parallel execution with Analysis node if possible.

### 4.3. Schedule Optimizer Agent (`schedule`)
-   **Role**: The "Brain" that solves the constraint satisfaction problem.
-   **Logic**:
    1.  Receives `analysis_result` and `calendar_context`.
    2.  Uses Chain-of-Thought (CoT) to find gaps that match user preferences.
    3.  Generates 3 distinct options (e.g., "Earliest", "Balanced", "Focus Optimized").
-   **Model**: High-reasoning model (e.g., Gemini Pro / GPT-4o).

### 4.4. Executor Node (`execute`)
-   **Role**: Commits changes to the external system.
-   **Tools**:
    -   `create_calendar_event(event_data)`
-   **Safety**: Only runs after Human Approval.

## 5. Model Context Protocol (MCP) & Tooling

We will adopt a standardized interface for tools to allow easy swapping of implementations (e.g., Google Calendar vs. Outlook vs. Local storage).

### 5.1. Tool Definitions
Tools will be defined using Pydantic `BaseModel` for arguments.

#### `CalendarTool`
```python
class DateRange(BaseModel):
    start: datetime
    end: datetime

@tool("get_calendar_events")
def get_calendar_events(range: DateRange) -> List[Event]:
    """Fetch events from the active calendar provider within the range."""
    # Logic to switch between Google/Outlook based on user_integrations table
```

#### `AvailabilityTool`
```python
@tool("find_free_slots")
def find_free_slots(duration_minutes: int, range: DateRange) -> List[TimeSlot]:
    """Finds free time slots of at least 'duration_minutes'."""
```

## 6. Data Intermediates & Output

### 6.1. Intermediates
Data passed between nodes should be immutable where possible.
-   `AnalysisObject`: JSON object stored in State.
-   `ProposedSchedule`: JSON list of options.

### 6.2. Final Output
The workflow executes and returns a `WorkflowResult` to the frontend.
```json
{
  "status": "success",
  "task_id": "123",
  "analysis": { ... },
  "options": [
    { "id": 1, "start": "10:00", "reason": "Free block" },
    { "id": 2, "start": "14:00", "reason": "After lunch" }
  ],
  "requires_confirmation": true
}
```

## 7. Implementation Plan

### Phase 1: Foundation (Current)
-   [x] Basic LangGraph setup.
-   [x] Mock LLM integration.
-   [x] Basic State definition.

### Phase 2: Real Intelligence (Next Steps)
-   [ ] **step_1**: Replace `MockLLM` with `ChatOpenAI`/`ChatGoogleGenerativeAI`.
-   [ ] **step_2**: Implement `Analyzer` node with structured output parsing (PydanticOutputParser).
-   [ ] **step_3**: Implement `CalendarTools` using the existing `services/calendar/` logic but wrapped as LangChain tools.

### Phase 3: Advanced Orchestration
-   [ ] **step_4**: Update `Graph` to include the Feedback Loop (Conditional Edges).
-   [ ] **step_5**: Implement `checkpointer` (e.g., using Postgres/Redis) to persist state between user interactions (waiting for approval).

## 8. Third-Party Tools & Resources

-   **LangChain**: Framework for tool calling and prompting.
-   **LangGraph**: Orchestration and state management.
-   **Pydantic**: Data validation.
-   **Redis (Future)**: Usage for persisting conversation/workflow threads.

## 9. Security & resources
-   **Secrets Management**: API Keys (OpenAI, Google) stored in `.env`, loaded via `pydantic-settings`.
-   **Rate Limiting**: Implement token bucket for LLM calls to prevent cost spikes.
-   **Data Privacy**: Only send necessary data (obfuscate PII/Task content if not needed) to LLM.

## 10. Agent Specific vs Shared Resources
-   **Shared**:
    -   `LLMClient`: Singleton instance (thread-safe).
    -   `DatabaseSession`: Async session factory.
    -   `CalendarClient`: OAuth client manager.
-   **Agent Specific**:
    -   `PromptTemplates`: Specific YAML instructions (Analyzer vs Scheduler).
    -   `Parser`: Output parsers specific to the node's task.
