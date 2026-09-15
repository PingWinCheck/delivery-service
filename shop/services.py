from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from shop.dao import ShopVersionDAO, ShopDAO
from shop.exceptions import ShopNotFoundException
from shop.models import Shop, ApplicationStatus
from datetime import datetime, timezone


class ShopAndShopVersionSyncRepository:
    def __init__(self,
                 session: AsyncSession,
                 shop: ShopDAO = ShopDAO,
                 shop_version: ShopVersionDAO = ShopVersionDAO,
                 ):
        self.session = session
        self.shop = shop
        self.shop_version = shop_version

    async def create(self, **kwargs) -> Shop:
        instance_shop = self.shop.model(**kwargs)
        self.session.add(instance_shop)
        await self.session.flush()

        instance_shop_version = self.shop_version.model(**kwargs, shop_id=instance_shop.id)
        self.session.add(instance_shop_version)
        await self.session.flush()
        return instance_shop

    # async def update_by_id(self,id_: int, **kwargs):
    #     shop = await self.shop.get_by_id(id_=id_, session=self.session)
    #     if shop is None:
    #         return None
    #     shop.

    async def get(self):
        pass


class ServiceShop:
    def __init__(self,
                 repository_shop: type["ShopDAO"],
                 repository_shop_history: type["ShopVersionDAO"]):
        self._repository_shop = repository_shop
        self._repository_shop_history = repository_shop_history

    async def get_all_applications_with_status(self,
                                   session: AsyncSession,
                                   status: "ApplicationStatus"):
        application_pending = await self._repository_shop.get_by_filter(session, status=status.value)
        return application_pending

    async def get_application_by_id(self,
                                    session: AsyncSession,
                                    id_: int):
        application = await self._repository_shop.get_by_id(session=session,
                                                                id_=id_)
        return application

    async def get_application_by_id_with_history(self,
                                    session: AsyncSession,
                                    id_: int):
        application = await self._repository_shop.get_by_id(session=session,
                                                                id_=id_)
        application_history = await self._repository_shop_history.get_by_filter(shop_id=application.id,
                                                                                session=session)
        return application, application_history

    async def change_application_status(self,
                                        session: AsyncSession,
                                        id_: int,
                                        reviewed_by_id: UUID,
                                        new_status: "ApplicationStatus",
                                        reason: str | None = None) -> "Shop":
        application = await self._repository_shop.get_by_id(id_=id_, session=session)
        if application is None:
            raise ShopNotFoundException(f'Магазин с id={id_} не найден')
        application.status = new_status
        application.reviewed_by_id = reviewed_by_id
        application.reason = reason
        application.reviewed_at = datetime.now(timezone.utc)

        await session.flush()

        session.add(self._repository_shop_history.model(
            shop_id=application.id,
            title=application.title,
            description=application.description,
            owner_id=application.owner_id,
            address_id=application.address_id,
            status=application.status,
            reviewed_at=application.reviewed_at,
            reviewed_by_id=application.reviewed_by_id,
            reason=application.reason
        ))

        await session.commit()

        return application