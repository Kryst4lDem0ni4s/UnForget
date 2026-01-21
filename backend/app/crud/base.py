
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.base import Base

class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[Base]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Base]:
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: Union[Dict[str, Any], Base]) -> Base:
        obj_in_data = obj_in.dict() if hasattr(obj_in, "dict") else obj_in
        if isinstance(obj_in_data, dict):
             db_obj = self.model(**obj_in_data)
        else:
            db_obj = self.model(**obj_in_data.dict()) 
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Base, obj_in: Union[Dict[str, Any], Base]) -> Base:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> Base:
        obj = await self.get(db, id)
        await db.delete(obj)
        await db.commit()
        return obj
