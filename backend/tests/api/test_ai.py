import pytest
from httpx import AsyncClient
from uuid import UUID

from app.models.user import User


@pytest.mark.asyncio
async def test_analyze_task_endpoint(client: AsyncClient, db_session, auth_headers):
    """Test AI task analysis endpoint."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="aitest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create a task
    task_response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Complex AI Project",
            "description": "Build an AI-powered scheduler",
            "priority": "high",
            "context_notes": "Requires deep focus and research"
        },
        headers=auth_headers
    )
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    
    # Analyze the task with AI
    analyze_response = await client.post(
        "/api/v1/ai/analyze-task",
        json={"task_id": task_id},
        headers=auth_headers
    )
    
    assert analyze_response.status_code == 200
    result = analyze_response.json()
    
    # Verify AI analysis
    assert result["task_id"] == task_id
    assert "estimated_duration_minutes" in result
    assert result["estimated_duration_minutes"] > 0
    assert "ai_reasoning" in result
    assert len(result["ai_reasoning"]) > 0


@pytest.mark.asyncio
async def test_schedule_task_endpoint(client: AsyncClient, db_session, auth_headers):
    """Test AI scheduling endpoint."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="scheduletest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create a task
    task_response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Meeting Preparation",
            "priority": "medium"
        },
        headers=auth_headers
    )
    task_id = task_response.json()["id"]
    
    # Get scheduling options
    schedule_response = await client.post(
        "/api/v1/ai/schedule",
        json={"task_id": task_id},
        headers=auth_headers
    )
    
    assert schedule_response.status_code == 200
    result = schedule_response.json()
    
    # Verify scheduling options
    assert result["task_id"] == task_id
    assert "options" in result
    assert len(result["options"]) == 3  # Should provide 3 options
    
    # Verify each option has required fields
    for option in result["options"]:
        assert "option_number" in option
        assert "start_time" in option
        assert "end_time" in option
        assert "reasoning" in option
        assert "impact" in option


@pytest.mark.asyncio
async def test_task_not_found_error(client: AsyncClient, db_session, auth_headers):
    """Test error handling for non-existent task."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="errortest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Try to analyze non-existent task
    response = await client.post(
        "/api/v1/ai/analyze-task",
        json={"task_id": "00000000-0000-0000-0000-999999999999"},
        headers=auth_headers
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_full_ai_workflow(client: AsyncClient, db_session, auth_headers):
    """Test complete workflow: Create task -> Analyze -> Schedule."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="workflow@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Step 1: Create task
    task_response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Write Documentation",
            "description": "Complete API documentation",
            "priority": "high",
            "context_notes": "Best done in the morning"
        },
        headers=auth_headers
    )
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    
    # Step 2: Analyze task
    analyze_response = await client.post(
        "/api/v1/ai/analyze-task",
        json={"task_id": task_id},
        headers=auth_headers
    )
    assert analyze_response.status_code == 200
    analysis = analyze_response.json()
    assert analysis["estimated_duration_minutes"] > 0
    
    # Step 3: Get scheduling options
    schedule_response = await client.post(
        "/api/v1/ai/schedule",
        json={"task_id": task_id},
        headers=auth_headers
    )
    assert schedule_response.status_code == 200
    schedule = schedule_response.json()
    assert len(schedule["options"]) == 3
    
    # Step 4: Verify task was updated with AI data
    task_get_response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )

@pytest.mark.asyncio
async def test_analyze_task_invalid_input(client: AsyncClient, db_session, auth_headers):
    """Test AI analysis with invalid input."""
    # Try to analyze with missing task_id
    response = await client.post(
        "/api/v1/ai/analyze-task",
        json={},
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_schedule_task_unauthorized(client: AsyncClient, db_session):
    """Test scheduling without auth."""
    response = await client.post(
        "/api/v1/ai/schedule",
        json={"task_id": "some-id"}
    )
    assert response.status_code == 403 or response.status_code == 401

@pytest.mark.asyncio
async def test_partial_task_data(client: AsyncClient, db_session, auth_headers):
    """Test analysis on task with minimal data."""
    # Create user
    from app.models.user import User
    test_user_id = "00000000-0000-0000-0000-000000000002"
    user = User(
        id=test_user_id,
        email="partial@test.com",
        auth_provider_id=test_user_id
    )
    db_session.add(user)
    await db_session.commit()
    
    # Create minimal task
    task_response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Minimal Task"},
        headers=auth_headers
    )
    task_id = task_response.json()["id"]
    
    # Analyze
    response = await client.post(
        "/api/v1/ai/analyze-task",
        json={"task_id": task_id},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["estimated_duration_minutes"] > 0
