from sqlalchemy import select, func

from typing import TYPE_CHECKING, Type, Sequence, ClassVar

if TYPE_CHECKING:
    from .database import Base
    from sqlalchemy.ext.asyncio import AsyncSession


class DAOBase[ModelT: Base]:
    #TODO Не совсем корректная аннотация типов, но =None нужно исключительно в рамках проверки на реализацию атрибута model
    model: ClassVar[type["ModelT"]] = None

    def __init_subclass__(cls, **kwargs):
        if cls.model is None:
            raise NotImplementedError('Необходимо указать модель')
        super().__init_subclass__(**kwargs)

    @classmethod
    async def get_by_id(cls, id_, session: "AsyncSession", ) -> ModelT | None:
        return await session.get(cls.model, id_)


    @classmethod
    async def get_by_filter(cls,
                            session: "AsyncSession",
                            limit: int | None = None,
                            offset: int | None = None,
                            **filter_) -> Sequence[ModelT] | None:
        query = select(cls.model)
        for key, value in filter_.items():
            if not hasattr(cls.model, key):
                raise AttributeError(f'Модель {cls.model.__name__} не имеет аттрибута {key}')
            query = query.filter(getattr(cls.model, key) == value)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await session.execute(query)
        return result.scalars().all()


    @classmethod
    async def create(cls, session: "AsyncSession", **kwargs) -> ModelT:
        instance = cls.model(**kwargs)
        session.add(instance)
        # await session.commit()
        await session.flush()
        return instance

    @classmethod
    async def count_with_filter_by(cls,
                         session: "AsyncSession",
                         **filter_by) -> int | None:
        query = (
            select(func.count(cls.model.id)).filter_by(**filter_by)
        )
        return (await session.execute(query)).scalar_one_or_none()

