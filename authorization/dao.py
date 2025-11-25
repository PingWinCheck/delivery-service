from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import DAOBase
from .models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import EmailStr
    from sqlalchemy.ext.asyncio import AsyncSession

class UserDAO(DAOBase):
    model = User

    @classmethod
    async def get_by_email(cls, email: "EmailStr", session: "AsyncSession") -> User:
        query = (select(cls.model).filter_by(email=email).options(joinedload(cls.model.role)))
        return await session.scalar(query)