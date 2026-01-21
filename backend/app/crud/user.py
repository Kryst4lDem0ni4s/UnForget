
from app.crud.base import CRUDBase
from app.models.user import User

class CRUDUser(CRUDBase):
    pass

user = CRUDUser(User)
