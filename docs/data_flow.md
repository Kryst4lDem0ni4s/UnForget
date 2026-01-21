# Data Flow & Communication Strategy

## 1. Task Creation & AI Analysis Flow
**Goal**: User creates a task, and the system estimates duration and suggests times.

1.  **Frontend**: User inputs "Complete the quarterly report" + Context "Need deep focus".
2.  **Frontend**: POST `/tasks` with `status=pending`.
3.  **Backend (API)**: Saves Task to DB. Returns `task_id`.
4.  **Backend (Service)**: Pushes Job `analyze_task(task_id)` to Redis Queue.
5.  **Backend (Worker)**:
    *   Pulls job.
    *   Fetches Task + User Context (ChromaDB).
    *   Calls **LangGraph Node: Analyze**.
    *   LLM Output: "Duration: 120m, Tag: Work/Deep".
    *   Updates Task in DB.
    *   Triggers **Schedule** Job.
6.  **Backend (Worker)**:
    *   Fetches `calendar_events` for user (Local Cache).
    *   Calls **LangGraph Node: Schedule**.
    *   LLM Output: [Option A (Tue 10am), Option B (Wed 2pm)].
    *   Saves Options to `scheduling_options` (Redis/Temp DB).
7.  **frontend**: Polls `/ai/schedule/status/{job_id}` (Simpler than WS for MVP).
8.  **Frontend**: Receiving "Complete", fetches Options. Displays Suggestion Cards.

## 2. Calendar Sync Flow (Bi-Directional)
**Goal**: Keep local cache in sync with Google/Outlook.

### Inbound (Google -> App)
1.  **Google**: User adds "Dentist Appointment" on GCal Web.
2.  **Google API**: Sends Webhook to `backend/api/v1/endpoints/calendar.py:webhook`.
3.  **Backend**:
    *   Validates `X-Goog-Channel-ID`.
    *   Enqueues `sync_calendar(user_id)` job.
4.  **Backend (Worker)**:
    *   Calls `GoogleCalendarService.list_events(updatedMin=last_sync)`.
    *   Upserts events to `calendar_events` table.
    *   **Crucial**: If a "Flexible" AI task now conflicts with this new Fixed event, Trigger `Reschedule` Job.

### Outbound (App -> Google)
1.  **Frontend**: User confirms AI Suggestion (Option A).
2.  **Backend**:
    *   Updates Task status `scheduled`.
    *   Creates Event in `calendar_events`.
    *   Calls `GoogleCalendarService.insert_event()`.

## 3. Local Mode Data Flow (Desktop)
**Goal**: Privacy-first AI.

1.  **Flutter Desktop**: Detects `Use Local AI` toggle.
2.  **Flutter Desktop**: Spawns `sidecar/main.py` subprocess (if not running).
3.  **Flutter**: Sends HTTP POST to `localhost:12345/analyze` (Local Sidecar) instead of Cloud API.
4.  **Sidecar**:
    *   Runs local langchain logic.
    *   Calls `localhost:11434` (Ollama).
    *   Returns JSON response to Flutter.
5.  **Data Sync**: Flutter *still* syncs the final Task/Event to Cloud API for backup (if enabled), but the *reasoning* happened locally.

## Communication Protocols
*   **Mobile <-> Cloud API**: REST (JSON) over HTTPS.
*   **Desktop <-> Sidecar**: REST (JSON) over HTTP (localhost).
*   **Backend <-> Redis**: TCP.
*   **Backend <-> Postgres**: TCP (Connection Pooled).

## Optimization Strategies
1.  **Optimistic UI**: Frontend adds the task to the list *immediately* as "Syncing...", doesn't wait for API.
2.  **Debounced Writes**: If user drags an event 5 times in 1 second, send only the final position.
3.  **Payload Minimization**: `/calendar/events` returns only essential fields (id, title, start, end, color). Details fetched on tap.
