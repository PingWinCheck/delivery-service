from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiohttp
from .schemas import LoginSchema
from core import conf, get_logger

from .utils import JWT

log = get_logger(__name__)

jwt = JWT(key=conf.jwt.public_key, algorithms=conf.jwt.algorithm)
router = APIRouter(prefix='/authorization')

@router.post('/proxy-login')
async def proxy_login(login: LoginSchema):
    async with aiohttp.ClientSession() as session:
        async with session.post(str(conf.login_proxy.url),
                                json={'email': login.email,
                                      'password': login.password}) as response:
            resp = await response.json()
            log.info('Post request: %r', conf.login_proxy.url)
            return JSONResponse(content=resp, status_code=response.status)

