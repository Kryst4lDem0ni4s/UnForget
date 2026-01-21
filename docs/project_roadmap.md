# Project Implementation Roadmap

## Phase 1: Foundation (Weeks 1-4)
**Goal**: Core skeleton, Auth, and Gamified UI.

### backend-infrastructure
- [x] **Scaffold FastAPI**: Setup project structure (SQLite/Async).
- [x] **DB Init**: SQLAlchemy schema with users, tasks, subscriptions.
- [x] **Auth**: Local/Mock integration (Bearer Token).
- [ ] **Tier Logic**: Middleware to check `tasks_usage_count` vs `subscription_tier`.

### flutter-frontend
- [ ] **Project Setup**: `flutter create`, add `riverpod`, `go_router`.
- [ ] **Cloud UI**: Implement `CustomPainter` for "Clear Sky" vs "Thunder" states.
- [ ] **Responsive Layout**: Sidebar for Desktop, BottomNav for Mobile.
- [ ] **Task Entry**: Form with "Context" and "AI Enhanced" fields (disabled for now).

---

## Phase 2: Integration Layer (Weeks 5-8)
**Goal**: External Calibration.

### backend-infrastructure
- [ ] **OAuth Endpoints**: `/auth/google` and `/auth/microsoft`.
- [ ] **Token Storage**: Encrypted `refresh_token` handling.
- [x] **Sync Engine**: API-based sync (`/sync`).
- [ ] **Webhooks**: Listener for Google Push Notifications.

### flutter-frontend
- [ ] **Calendar Widget**: Integrate `syncfusion_flutter_calendar`.
- [ ] **Sync visualizer**: Show "Syncing..." status.

---

## Phase 3: AI Engine (Weeks 9-14)
**Goal**: The "Brain" of the planner.

### ai-pipeline
- [x] **LangGraph Setup**: StateGraph (`Analyze` -> `Schedule` -> `Review` -> `Execute`).
- [x] **Task Analysis Node**:
    - Input: Task Description.
    - Output: Duration, Priority, Tags.
    - Model: Ollama/Mock.
- [x] **Calendar Scan Node**: Filter "Fixed" vs "Flexible" slots.
- [x] **Scheduling Node**:
    - Logic: Find slots via LLM.
    - Reasoning: Generate text.
    - Model: Ollama/Mock.
- [x] **Local Fallback**: `llm_factory` switching to `MockLLM` if Ollama offline.

### backend-infrastructure
- [x] **API Endpoints**: `/start`, `/status`, `/resume` (Async).
- [ ] **Rate Limiter**: Enforce 10 tasks/mo for Free tier.

---

## Phase 4: UI Polish & Human-in-Loop (Weeks 15-18)
**Goal**: Seamless User Experience.

### flutter-frontend
- [ ] **Suggestion Cards**: UI for the 3 AI options (Accept/Reject).
- [ ] **Gamification Logic**: Link Task Completion -> Cloud Animation state.
- [ ] **Drag & Drop**: Manual override of AI choices.

### integration-testing
- [ ] **E2E Tests**: Full flow from "Add Task" -> "AI Suggestion" -> "GCal Sync".

---

## Phase 5: Testing & Launch (Weeks 19-22)
**Goal**: Production Readiness.

### security-compliance
- [ ] **Pen Test**: Run OWASP ZAP on API.
- [ ] **GDPR Check**: Test "Delete Account" flow.

### infrastructure-provisioning
- [ ] **Staging Deploy**: Deploy to AWS/GCP Staging.
- [ ] **Load Test**: Simulate 1000 concurrent users.

### ci-cd-pipeline
- [ ] **Production Release**: Automated pipeline to App Stores.
