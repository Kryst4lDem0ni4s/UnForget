# Project Directory Structure (Detailed)

This document defines the exact file organization for the AI Planner MVP. We utilize a **Monorepo** structure for code cohesion during the MVP phase.

```text
/
├── .antigravity/                 # Agent configuration
├── .github/                      # CI/CD workflows
├── frontend/                     # Flutter App (Android/iOS)
│   ├── lib/
│   │   ├── core/             # Shared utilities, theme, constants
│   │   ├── features/         # Feature-first modules
│   │   │   ├── auth/         # Login screens, providers
│   │   │   ├── calendar/     # Calendar widget, riverpod providers
│   │   │   ├── tasks/        # Task list, add task form
│   │   │   ├── gamification/ # Cloud rendering logic
│   │   │   └── ai_assistant/ # Suggestion cards UI
│   │   ├── services/         # API Clients (Dio)
│   │   └── main.dart         # Entry point
│   ├── assets/               # Lottie files, images
│   └── pubspec.yaml
│
├── backend/                      # FastAPI Modular Monolith
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── tasks.py
│   │   │   │   │   ├── calendar.py
│   │   │   │   │   └── ai.py
│   │   │   │   └── api.py        # Router configuration
│   │   │   └── deps.py           # Dependency Injection (DB, User)
│   │   │
│   │   ├── core/
│   │   │   ├── config.py         # Settings (Env vars)
│   │   │   └── security.py       # JWT/Auth logic
│   │   │
│   │   ├── db/
│   │   │   ├── base.py           # SQLAlchemy Base
│   │   │   ├── session.py        # DB Session factory
│   │   │   └── init_db.py        # Seed data
│   │   │
│   │   ├── models/               # SQLAlchemy Models
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── event.py
│   │   │
│   │   ├── schemas/              # Pydantic Schemas (Request/Response)
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── event.py
│   │   │
│   │   ├── services/             # Business Logic (The "Microservice" boundaries)
│   │   │   ├── calendar_sync/    # Google/MS Graph logic
│   │   │   │   ├── google.py
│   │   │   │   └── microsoft.py
│   │   │   └── ai_pipeline/      # LangGraph invocation
│   │   │       ├── graph.py
│   │   │       ├── nodes/
│   │   │       │   ├── analyze.py
│   │   │       │   └── schedule.py
│   │   │       └── prompts/      # YAML Prompt templates
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/                  # DB Migrations
│   ├── tests/                    # Pytest
│   ├── Dockerfile
│   └── requirements.txt
│
├── shared/                       # Shared logic (if any)
└── docs/                         # Architecture documentation
```

## Key Decisions
1.  **Feature-First Flutter**: Organizing by feature (`calendar`, `tasks`) scales better than by type (`screens`, `widgets`).
2.  **Modular Monolith Backend**: The `services/` directory isolates business logic. `calendar_sync` needs no knowledge of `ai_pipeline` internals, only its public interface. This allows us to split them into separate microservices later *if needed*.
3.  **Sidecar Pattern**: The `apps/desktop/sidecar` folder contains the Python code that runs LOCALLY on the user's machine for the "Local AI" feature. It mimics the interface of the `backend/` API but routes to Ollama.
