# Tech Stack & Microservice Boundaries

## Technology Stack

### Frontend (Mobile & Desktop)
| Component | Choice | Reason |
| :--- | :--- | :--- |
| **Framework** | **Flutter 3.x** | Single codebase for iOS, Android, Windows, Mac. |
| **Language** | **Dart** | Strongly typed, AOT compiled for performance. |
| **State** | **Riverpod** | Compile-safe dependency injection and state management. |
| **HTTP** | **Dio** | Robust interceptors, cancellation, transformers. |
| **Local DB** | **Hive** | NoSQL, extremely fast, pure Dart (no native bridges needed). |
| **Calendar** | **syncfusion_flutter_calendar** | Production-ready drag-and-drop, rich views. |
| **Gamification** | **CustomPainter + Lottie** | High performant custom rendering. |

### Backend (Cloud)
| Component | Choice | Reason |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | High perf (Starlette), Async, Auto OpenAPI docs. |
| **Language** | **Python 3.11** | Native home of LangChain/LangGraph and AI libs. |
| **DB ORM** | **SQLAlchemy 2.0 (Async)** | Modern async support, robust mapping. |
| **Migrations** | **Alembic** | Standard for SQLAlchemy. |
| **Queue** | **Redis** | Simple, fast broker for Celery/ARQ. |
| **Orchestrator**| **LangGraph** | Best for stateful, cyclic agent workflows. |

### Infrastructure (DevOps)
| Component | Choice | Reason |
| :--- | :--- | :--- |
| **Container** | **Docker** | Standard deployment unit. |
| **Auth** | **Firebase Auth** | Free tier is generous, handles email/social logins easily. |
| **Reverse Proxy**| **Nginx / Cloud Load Balancer** | SSL termination, routing. |

## Microservice Boundaries (Logical -> Physical)

For the MVP, we adopt a **Modular Monolith**. We define strict logical boundaries now so we can split them later without refactoring usage code.

### 1. **Core Service** (`app.core`, `app.api`)
*   **Responsibility**: Auth, Routing, Rate Limiting.
*   **Shared**: Yes.

### 2. **Task Service** (`app.services.tasks`)
*   **Responsibility**: CRUD on Tasks.
*   **Dependencies**: Database.
*   **Future Split**: Standalone Task Microservice.

### 3. **Sync Service** (`app.services.calendar_sync`)
*   **Responsibility**: Talking to Google/MS APIs.
*   **Dependencies**: `user_integrations` table (tokens).
*   **Scale**: This is the "noisy" neighbor. Good candidate to split first if polling load gets high.

### 4. **Intelligence Service** (`app.services.ai_pipeline`)
*   **Responsibility**: CPU/GPU intensive reasoning.
*   **Dependencies**: Redis Queue, Vector DB.
*   **Isolation**: Runs in background workers (Celery), separate from API nodes.

## Cost Minimization Strategy
1.  **Stateless Compute**: Run FastAPI on **Cloud Run** (Scale to Zero) or AWS Lambda. Pay only when active.
2.  **Database**: Start with minimal Managed Postgres (e.g., Supabase Free Tier or Neon).
3.  **Caching**: Aggressive caching of Calendar Events in Redis to avoid hitting Google API quotas.
4.  **Local First**: Encourage Desktop users to use "Local Mode" -> Zero Cloud Compute cost for AI.
