# Backend Setup Instructions

## Prerequisites
1. **Python 3.11+** installed
2. **PostgreSQL** installed and running locally
3. **Redis** installed and running locally (optional for basic testing)

## Quick Start (Without Docker)

### 1. Install Dependencies
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

Update `.env` with your local database credentials:
```
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/aiplanner
```

### 3. Create Database
Using PostgreSQL:
```sql
CREATE DATABASE aiplanner;
```

### 4. Run Migrations
```powershell
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Start the Server
```powershell
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## With Docker (Recommended)

Make sure Docker Desktop is running, then:

```powershell
# Start all services
docker-compose up -d

# Create and apply migrations
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs -f backend
```

## Testing Authentication

Use the mock auth token in requests:
```bash
curl -H "Authorization: Bearer test-user" http://localhost:8000/api/v1/users/me
```

## Creating a Test User

First, create a user (this will create the user with the test ID):
```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "auth_provider_id": "00000000-0000-0000-0000-000000000001"
  }'
```
