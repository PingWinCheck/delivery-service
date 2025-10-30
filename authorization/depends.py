from typing import Annotated

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core import conf
from .utils import JWT

# bearer = OAuth2PasswordBearer(tokenUrl='authorization/proxy-login')
bearer = OAuth2PasswordBearer(tokenUrl=str(conf.login_proxy.url))
jwt = JWT(key=conf.jwt.public_key, algorithms=conf.jwt.algorithm)

async def token(jwt_token: Annotated[str, Depends(bearer)]):
    payload = jwt.decode(jwt_token)
    return payload