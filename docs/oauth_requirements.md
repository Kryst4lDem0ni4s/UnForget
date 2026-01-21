# OAuth Integration Requirements

## 1. Google Calendar Integration
**Scope**: `https://www.googleapis.com/auth/calendar`

### Flow
1.  Frontend initiates OAuth 2.0 flow via Firebase Auth or Google Sign-In.
2.  Backend receives `auth_code` or `access_token` (depending on implementation choice for offline access).
3.  **Critical**: For server-side sync (AI Agents modifying calendar), Backend needs a **Refresh Token**.
4.  Store Refresh Token securely (Encrypted) in `users` or a separate `user_credentials` table.

### Sync Logic
- **Incoming**: Webhook (Push Notifications) from Google Calendar API to `/webhooks/google/calendar`.
- **Outgoing**: AI Agent calls `calendar.events.insert` or `patch`.

## 2. Microsoft Graph Integration (To Do & Calendar)
**Scope**: `Calendars.ReadWrite`, `Tasks.ReadWrite`

### Flow
1.  Similar OAuth 2.0 flow against Azure AD endpoint.
2.  Requires App Registration in Azure Portal.
3.  Store Refresh Token.

### Sync Logic
- **Incoming**: Graph API allows delta queries ( `/me/calendarView/delta`) for efficient sync.
- **Outgoing**: POST to `/me/events` or `/me/todo/lists`.

## 3. Privacy & Security
- **Encryption**: All tokens MUST be encrypted using AES-256 before storage in the DB.
- **Access Control**: Only the "Backend Infrastructure Agent" should have access to the decryption keys.
- **User Revocation**: Provide an endpoint `/auth/disconnect/{provider}` to delete tokens.

## 4. Local/Offline Considerations
- If the user is running `ollama` locally, the "AI Pipeline Agent" might run on the Desktop Client directly instead of the Cloud Backend.
- **Hybrid Architecture**:
    - **Mobile**: Always talks to Cloud API.
    - **Desktop**: Can toggle "Local Agent". In this case, the Desktop App needs to talk to Google/MS APIs directly (Client-side sync) OR the Cloud Backend still handles Sync, but the "Thinking" happens locally and sends results to Backend.
    - **Decision**: MVP will centralize Integrations in Backend to keep data consistent. Desktop "Local Model" will simply be an API provider override (Desktop runs Ollama, exposes port, Backend *could* potentially call it if standard, OR Desktop App computes logic and sends *result* to Backend.
    - **Refined Decision**: For MVP simplicity, **Local Models (Ollama)** imply the AI processing happens on the Desktop App.
        - Desktop App: LangGraph runs in Python process on user machine? Or embedded Lib?
        - **Simpler**: Desktop App has a local Python sidecar (PyInstaller) that runs FastAPI + LangGraph locally.
        - **Implication**: We need a "Shared" architecture where the Backend Logic can run both in Cloud (for Mobile/Web) and Local (for Desktop Privacy).
