from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from authorization.depends import get_user
from shop.dao import AddressDAO, ShopDAO, ShopVersionDAO
from shop.geocode import get_geocode
from shop.schemas import ShopSchema, ResponseCreateShopApplication, ChangeApplication
from core.dependencies import get_async_session
from shop.dependencies import service_shop
from shop.models import ApplicationStatus


if TYPE_CHECKING:
    from authorization.models import User



router = APIRouter(prefix='/shop')

@router.post('/request-to-create-a-store', response_model=ResponseCreateShopApplication)
async def request_to_create_a_store(user: Annotated["User", Depends(get_user)],
                                    shop: ShopSchema,
                                    session: Annotated[AsyncSession, Depends(get_async_session)]):
    #TODO: вынести логику в отельный сервис
    address_raw = f'{shop.address.city} {shop.address.street} {shop.address.home}'
    geocode = await get_geocode(address_raw)
    try:
        address = await AddressDAO.create(session=session,
                                          city=geocode.raw["properties"]['city'],
                                          street=geocode.raw["properties"]['street'],
                                          home=geocode.raw["properties"]['housenumber'],
                                          latitude=geocode.latitude,
                                          longitude=geocode.longitude,
                                         )


        shop_application = await ShopDAO.create(session=session,
                             **shop.model_dump(exclude={'address'}),
                             owner_id=user.id,
                             address_id=address.id)

        await ShopVersionDAO.create(session=session,
                                    **shop.model_dump(exclude={'address'}),
                                    shop_id=shop_application.id,
                                    owner_id=user.id,
                                    address_id=address.id)

        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Магазин с названием <{shop.title}> уже существует')
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Недоступен сервис')


    return shop_application


@router.get('/application')
async def get_application(id_: int,
                          user: Annotated["User", Security(get_user, scopes=['d-application-read'])],
                          session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await service_shop.get_application_by_id(session, id_)
    return result

@router.get('/applications')
async def get_applications(status: ApplicationStatus,
                           # user: Annotated["User", Security(get_user, scopes=['d-applications-read'])],
                           session: Annotated[AsyncSession, Depends(get_async_session)],
                           ):
    result = await service_shop.get_all_applications_with_status(session, status=status)
    return result

@router.patch('/application')
async def change_status_application(change: ChangeApplication,
                                    user: Annotated["User", Security(get_user, scopes=['d-application-patch'])],
                                    session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await service_shop.change_application_status(session=session,
                                                    id_=change.id,
                                                    reviewed_by_id=user.id,
                                                    reason=change.reason,
                                                    new_status=change.status)
    return result