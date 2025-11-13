from sqlalchemy import select

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .database import Base
    from sqlalchemy.ext.asyncio import AsyncSession


class DAO:
    model: Type[Base] = None

    def __init__(self, session: "AsyncSession"):
        self.session = session

    def __init_subclass__(cls, **kwargs):
        if cls.model is None:
            raise NotImplementedError('Необходимо указать модель')
        super().__init_subclass__(**kwargs)

    async def get_by_id(self, id_):
        return await self.session.get(self.model, id_)

    async def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
