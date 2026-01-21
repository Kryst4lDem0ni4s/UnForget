import pytest
from httpx import AsyncClient
from uuid import UUID

from app.models.user import User


@pytest.mark.asyncio
async def test_calendar_sync_google(client: AsyncClient, db_session, auth_headers):
    """Test Google Calendar sync endpoint."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="caltest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Test calendar sync
    response = await client.post(
        "/api/v1/calendar/sync",
        json={"provider": "google"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "status" in result
    assert "events_synced" in result


@pytest.mark.asyncio
async def test_calendar_sync_microsoft(client: AsyncClient, db_session, auth_headers):
    """Test Microsoft Calendar sync endpoint."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="mstest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Test calendar sync
    response = await client.post(
        "/api/v1/calendar/sync",
        json={"provider": "microsoft"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "status" in result


@pytest.mark.asyncio
async def test_calendar_invalid_provider(client: AsyncClient, db_session, auth_headers):
    """Test calendar sync with invalid provider."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="invalidtest@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Test with invalid provider
    response = await client.post(
        "/api/v1/calendar/sync",
        json={"provider": "invalid"},
        headers=auth_headers
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_calendar_events(client: AsyncClient, db_session, auth_headers):
    """Test listing calendar events."""
    # Create test user
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user = User(
        id=test_user_id,

        email="listevents@example.com",
        auth_provider_id=test_user_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # List events
    response = await client.get(
        "/api/v1/calendar/events",
        headers=auth_headers
    )
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_calendar_sync_no_provider(client: AsyncClient, db_session, auth_headers):
    """Test sync request without provider."""
    response = await client.post(
        "/api/v1/calendar/sync",
        json={},
        headers=auth_headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_calendar_sync_unauthorized(client: AsyncClient):
    """Test sync without auth."""
    response = await client.post(
        "/api/v1/calendar/sync",
        json={"provider": "google"}
    )
    assert response.status_code == 403 or response.status_code == 401
