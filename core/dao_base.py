from sqlalchemy import select

from typing import TYPE_CHECKING, Type, Sequence

if TYPE_CHECKING:
    from .database import Base
    from sqlalchemy.ext.asyncio import AsyncSession


class DAOBase:
    model: Type["Base"] = None

    def __init_subclass__(cls, **kwargs):
        if cls.model is None:
            raise NotImplementedError('Необходимо указать модель')
        super().__init_subclass__(**kwargs)

    @classmethod
    async def get_by_id(cls, id_, session: "AsyncSession", ) -> "Base":
        return await session.get(cls.model, id_)

#TODO: Не работает вроде
    @classmethod
    async def get_by_filter(cls, session: "AsyncSession", **filter_) -> Sequence["Base"]:
        query = select(cls.model)
        for key, value in filter_.items():
            if not hasattr(cls.model, key):
                raise AttributeError(f'Модель {cls.model.__name__} не имеет аттрибута {key}')
            query = query.filter(key == value)
        result = await session.execute(query)
        return result.scalars().all()


    @classmethod
    async def create(cls, session: "AsyncSession", **kwargs) -> "Base":
        instance = cls.model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
