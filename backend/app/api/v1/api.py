
from fastapi import APIRouter
from app.api.v1.endpoints import tasks, users, ai, calendar

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
