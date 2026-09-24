from fastapi import Query

from .database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Annotated
from core.schemas import PagerInputSchema, PagerOutputSchema

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def pager(pagers: Annotated[PagerInputSchema, Query()]):
    offset = (pagers.page - 1) * pagers.size
    return PagerOutputSchema(limit=pagers.size,
                             offset=offset)
