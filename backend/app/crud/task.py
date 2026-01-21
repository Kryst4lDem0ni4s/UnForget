
from app.crud.base import CRUDBase
from app.models.task import Task

class CRUDTask(CRUDBase):
    pass

task = CRUDTask(Task)
