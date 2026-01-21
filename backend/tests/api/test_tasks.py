
import pytest
from httpx import AsyncClient
from uuid import UUID

from app.models.user import User


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, db_session, auth_headers):
    """Test task creation."""
    # Create test user first
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="tasktest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create task
    task_data = {
        "title": "Complete quarterly report",
        "description": "Finish Q4 analysis",
        "priority": "high",
        "context_notes": "Need deep focus time"
    }
    
    response = await client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["status"] == "pending"
    assert data["user_id"] == test_user_id


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient, db_session, auth_headers):
    """Test listing tasks."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="listtest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create multiple tasks
    for i in range(3):
        await client.post(
            "/api/v1/tasks/",
            json={"title": f"Task {i}"},
            headers=auth_headers
        )
    
    # List tasks
    response = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient, db_session, auth_headers):
    """Test getting a specific task."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="gettest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create task
    create_response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Get task
    response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


@pytest.mark.asyncio
async def test_task_requires_auth(client: AsyncClient):
    """Test that task endpoints require authentication."""
    response = await client.post("/api/v1/tasks/", json={"title": "Test"})
    assert response.status_code == 403
    
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 403
