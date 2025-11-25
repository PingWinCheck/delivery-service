from core import DAOBase
from .models import User


class UserDAO(DAOBase):
    model = User
