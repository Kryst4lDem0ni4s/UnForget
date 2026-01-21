
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app import crud, schemas
from app.models.user import User


@pytest.mark.asyncio
async def test_create_user_crud(db_session: AsyncSession):
    """Test user CRUD creation."""
    user_in = schemas.UserCreate(
        email="crud@example.com",
        auth_provider_id="test-id"
    )
    
    user = await crud.user.create(db=db_session, obj_in=user_in)
    
    assert user.email == "crud@example.com"
    assert user.subscription_tier == "free"
    assert user.id is not None


@pytest.mark.asyncio
async def test_get_user_crud(db_session: AsyncSession):
    """Test getting user by ID."""
    # Create user
    user_in = schemas.UserCreate(
        email="getuser@example.com",
        auth_provider_id="test-id"
    )
    created_user = await crud.user.create(db=db_session, obj_in=user_in)
    
    # Get user
    retrieved_user = await crud.user.get(db=db_session, id=created_user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.email == "getuser@example.com"


@pytest.mark.asyncio
async def test_update_user_crud(db_session: AsyncSession):
    """Test updating user."""
    # Create user
    user_in = schemas.UserCreate(
        email="update@example.com",
        auth_provider_id="test-id"
    )
    user = await crud.user.create(db=db_session, obj_in=user_in)
    
    # Update user
    update_data = {"subscription_tier": "pro"}
    updated_user = await crud.user.update(
        db=db_session,
        db_obj=user,
        obj_in=update_data
    )
    
    assert updated_user.subscription_tier == "pro"


@pytest.mark.asyncio
async def test_list_users_crud(db_session: AsyncSession):
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        user_in = schemas.UserCreate(
            email=f"user{i}@example.com",
            auth_provider_id=f"test-id-{i}"
        )
        await crud.user.create(db=db_session, obj_in=user_in)
    
    # Get users
    users = await crud.user.get_multi(db=db_session, skip=0, limit=3)
    
    assert len(users) == 3
