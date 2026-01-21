
import pytest
from httpx import AsyncClient
from uuid import UUID

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db_session):
    """Test user creation."""
    user_data = {
        "email": "test@example.com",
        "auth_provider_id": "test-auth-id"
    }
    
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert data["subscription_tier"] == "free"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, db_session, auth_headers):
    """Test getting current user with auth."""
    # First create a test user with the expected ID
    test_user_id = "00000000-0000-0000-0000-000000000001"
    user_in = schemas.UserCreate(
        email="testuser@example.com",
        auth_provider_id=test_user_id
    )
    
    # Manually create user with specific ID
    from app.models.user import User
    from uuid import UUID
    
    user = User(
        id=UUID(test_user_id),
        email=user_in.email,
        auth_provider_id=user_in.auth_provider_id,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Now test the endpoint
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "testuser@example.com"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test that endpoints require authentication."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 403  # No auth header


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    """Test invalid authentication token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
