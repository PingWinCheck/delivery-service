from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import aiohttp
from .schemas import LoginSchema
from core import conf, get_logger
from .depends import token
from .utils import JWT

from fastapi.security import OAuth2PasswordRequestForm

log = get_logger(__name__)

jwt = JWT(key=conf.jwt.public_key, algorithms=conf.jwt.algorithm)
router = APIRouter(prefix='/authorization')

@router.post('/proxy-login')
async def proxy_login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    async with aiohttp.ClientSession() as session:
        async with session.post(str(conf.login_proxy.url),
                                json={'email': credentials.username,
                                      'password': credentials.password}) as response:
            resp = await response.json()
            log.info('Post request: %r, email: %r',
                     conf.login_proxy.url, credentials.username)
            return JSONResponse(content=resp, status_code=response.status)


@router.get('/secret')
async def secret(payload: Annotated[dict, Depends(token)]):
    return payload