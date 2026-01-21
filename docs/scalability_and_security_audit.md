# Scalability & Security Stress Test Audit

## 1. Scalability Analysis

### 1.1 Database Scalability (PostgreSQL)
*   **Current Design**: Single writer node.
*   **Bottleneck Risk**: High write throughput from "Real-time updates" and webhook listeners.
*   **Mitigation Strategy**:
    *   **Read Replicas**: Separate read/write traffic. The "Task Analysis" and "Calendar Scan" agents are read-heavy.
    *   **Partitioning**: Partition `calendar_events` table by `user_id` or `timestamp` (monthly) to keep index size manageable.
    *   **Connection Pooling**: Use `PgBouncer` middleware to handle thousands of concurrent Lambda/Serverless connections.

### 1.2 AI Processing Queue (Redis)
*   **Current Design**: Single Redis instance for task queues.
*   **Bottleneck Risk**: AI processing takes 5-30 seconds. A burst of 1000 users adding tasks simultaneously could flood the memory.
*   **Mitigation Strategy**:
    *   **Redis Cluster**: Sharding for higher throughput.
    *   **Back-pressure**: Implement `Leaky Bucket` rate limiting at the API Gateway level (FastAPI + Redis) BEFORE the queue.
    *   **Priority Queues**: Separate queues for "Pro" users (High Priority) vs "Free" users (Low Priority) as per the pricing model.

### 1.3 WebSocket/Real-time Updates
*   **Current Design**: Notification to frontend when AI finishes.
*   **Bottleneck Risk**: Maintaining thousands of open WebSocket connections consumes server file descriptors and memory.
*   **Mitigation Strategy**:
    *   **Server Push Notifications (FCM/APNS)**: For mobile, avoid persistent WebSockets. Use standard Push.
    *   **SSE (Server Sent Events)**: For Desktop/Web, lighter weight than WebSockets for one-way updates.

### 1.4 storage Cost (Gamification Assets)
*   **Current Design**: Lottie files and images.
*   **Optimization**:
    *   Use **Vector (Lottie)** over Raster assets.
    *   Cache assets endlessly on CDN (Cloudflare) with immutable versioning.

## 2. Security "Red Team" Audit

### 2.1 OAuth Token Storage
*   **Vulnerability**: If DB is compromised, refresh tokens allow attackers permanent access to user calendars.
*   **Stress Test**: SQL Injection on `/tasks` endpoint.
*   **Defense**:
    *   **Column-Level Encryption**: Encrypt `refresh_token` column using a key stored in a dedicated Secret Manager (AWS Secrets Manager / Vault), NOT in the app config.
    *   **Scope Minimization**: Request only minimum scopes.

### 2.2 Local Model (Ollama) Attack Vector
*   **Vulnerability**: A malicious task description could contain "Jailbreak" prompts to manipulate the Local LLM or Cloud LLM.
*   **Scenario**: User inputs malicious text that causes the Scheduling Agent to delete events.
*   **Defense**:
    *   **Input Sanitization**: Strict validation of "Task Description" length and characters.
    *   **System Prompt Hardening**: "You are a scheduler. You cannot delete events without explicit ID confirmation."
    *   **Sandboxing**: The Local Agent (Ollama) should run in a restricted container/sandbox on the desktop, limited network access.

### 2.3 Tier Abuse (Free Tier)
*   **Vulnerability**: User creates multiple accounts to bypass the "10 tasks/month" limit.
*   **Defense**:
    *   **Device Fingerprinting**: Link usage to Device ID, not just Email.
    *   **Phone Verification**: Require SMS verification for Basic/Pro tiers (optional, high friction but secure).

### 2.4 Data Privacy (GDPR)
*   **Requirement**: "Right to be Forgotten".
*   **Gap**: AI Context Vector DB (ChromaDB) might retain user data after account deletion.
*   **Fix**: Ensure `DELETE /user/{id}` cascades to:
    1.  Postgres User Record.
    2.  ChromaDB Vectors (Filter by metadata `user_id`).
    3.  Redis Queue pending jobs.

## 3. Failure Scenarios

| Scenario | Impact | Recovery Strategy |
| :--- | :--- | :--- |
| **Google/MS API Outage** | Calibration fails, Sync fails | Circuit Breaker pattern. Queue sync jobs with exponential backoff. Notify user "Sync Delayed". |
| **AI Model Hallucination** | Schedules meeting at 3 AM | **Heuristic Guardrails**: Logic layer checks `start_time` against `user.work_hours` before saving. |
| **Redis Crash** | Loss of pending schedule jobs | Use Redis AOF (Append Only File) persistence. Frontend retry mechanism if no response in 60s. |
| **Local Ollama Unresponsive** | Desktop AI fails | Fallback to Cloud API (if user permits) or Show "Local AI Unavailable" error. |
