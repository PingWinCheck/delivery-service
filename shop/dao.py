from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.dao_base import DAOBase
from shop.models import Shop, ShopVersion, Address

class ShopDAO(DAOBase[Shop]):
    model = Shop

    @classmethod
    async def get_by_id(cls,
                        id_,
                        session: "AsyncSession",
                        *,
                        owner: bool = False,
                        reviewed_by: bool = False
                        ) -> model | None:
        options = []
        if owner:
            options.append(joinedload(cls.model.owner))
        if reviewed_by:
            options.append(joinedload(cls.model.reviewed_by))

        return await session.get(cls.model, id_, options=options)


class ShopVersionDAO(DAOBase[ShopVersion]):
    model = ShopVersion


class AddressDAO(DAOBase[Address]):
    model = Address

