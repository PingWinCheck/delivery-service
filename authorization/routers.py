from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import LoginSchema
from core import conf, get_logger, get_async_session
from .depends import token, get_user
from .utils import JWT

from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes



if TYPE_CHECKING:
    from .models import User

log = get_logger(__name__)

jwt = JWT(key=conf.jwt.public_key, algorithms=conf.jwt.algorithm)
router = APIRouter(prefix='/authorization')

@router.post('/proxy-login')
async def proxy_login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    async with aiohttp.ClientSession() as session:
        async with session.post(str(conf.login_proxy.url),
                                data={'username': credentials.username,
                                      'password': credentials.password}) as response:
            resp = await response.json()
            log.info('Post request: %r, email: %r',
                     conf.login_proxy.url, credentials.username)
            return JSONResponse(content=resp, status_code=response.status)


