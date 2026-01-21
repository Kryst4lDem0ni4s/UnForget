# How to Use the AI Planner Agents

This project uses a multi-agent architecture to handle different aspects of development.

## Setup
Ensure you have the following configured in `.antigravity/`:
- `agent-permissions.yaml`: Defines what each agent can do.
- `security.yaml`: Security policies.
- `models.yaml`: Which LLM models are used by which agent.

## Available Agents
You can invoke these agents using their directive names.

1.  **Solution Architect** (`directives/solution_architect.md`)
    - *Use for*: System design, API changes, schema updates.
    - *Example*: "@[solution_architect.md] Design the schema for recurring tasks."

2.  **Backend Infrastructure** (`directives/backend_infrastructure.md`)
    - *Use for*: API endpoints, database migrations, server setup.
    - *Example*: "@[backend_infrastructure.md] Implement the /calendar/sync endpoint."

3.  **AI Pipeline** (`directives/ai_pipeline.md`)
    - *Use for*: LangGraph workflows, prompt engineering, AI logic.
    - *Example*: "@[ai_pipeline.md] Optimize the task complexity scoring node."

4.  **Flutter Frontend** (`directives/flutter_frontend.md`)
    - *Use for*: UI/UX, Widgets, Flutter logic.
    - *Example*: "@[flutter_frontend.md] Create the TaskCard widget with animations."

5.  **Integration Testing** (`directives/integration_testing.md`)
    - *Use for*: Writing and running tests.
    - *Example*: "@[integration_testing.md] writes tests for the login flow."

6.  **Security & Compliance** (`directives/security_compliance.md`)
    - *Use for*: Audits, vulnerability scans.
    - *Example*: "@[security_compliance.md] Check for hardcoded secrets."

7.  **CI/CD Pipeline** (`directives/cicd_pipeline.md`)
    - *Use for*: GitHub Actions, build scripts.
    - *Example*: "@[cicd_pipeline.md] Fix the specialized build step."

8.  **Infrastructure Provisioning** (`directives/infrastructure_provisioning.md`)
    - *Use for*: Terraform, cloud resources.
    - *Example*: "@[infrastructure_provisioning.md] Add a Redis cluster to the terraform config."

9.  **Observability & Monitoring** (`directives/observability_monitoring.md`)
    - *Use for*: Logging, Grafana dashboards.
    - *Example*: "@[observability_monitoring.md] Create a dashboard for API latency."

## Workflow
1.  **Plan**: Start with the Solution Architect to define *what* to build.
2.  **Build**: Use Backend and Frontend agents to implement the design.
3.  **Verify**: Use Integration Testing and Security agents to check the work.
4.  **Deploy**: Use CI/CD and Infrastructure agents to ship it.
5.  **Monitor**: Keep an eye on it with the Observability agent.

Happy coding!
