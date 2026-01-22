
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps
from app.core import security

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(security.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve tasks for current user.
    """
    # TODO: Filter tasks by user_id in CRUD
    tasks = await crud.task.get_multi(db, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Create new task for current user.
    """
    # Create task data with user_id
    task_data = task_in.dict()
    task_data["user_id"] = current_user.id
    
    task = await crud.task.create(db=db, obj_in=task_data)
    return task

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: str,
) -> Any:
    """
    Get task by ID.
    """
    task = await crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: str,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Update a task.
    """
    task = await crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.user_id != current_user.id:
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    task = await crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return task

@router.delete("/{task_id}", response_model=schemas.Task)
async def delete_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: str,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Delete a task.
    """
    task = await crud.task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.user_id != current_user.id:
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    task = await crud.task.remove(db=db, id=task_id)
    return task
