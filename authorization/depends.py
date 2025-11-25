from typing import Annotated, TYPE_CHECKING, Sequence

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import ellipses_string

from core import conf, get_async_session
from .schemas import JWTSchema
from .utils import JWT
from .dao import UserDAO
from .models import User

# bearer = OAuth2PasswordBearer(tokenUrl='authorization/proxy-login')
bearer = OAuth2PasswordBearer(tokenUrl=str(conf.login_proxy.url))
jwt = JWT(key=conf.jwt.public_key, algorithms=conf.jwt.algorithm)

async def token(jwt_token: Annotated[str, Depends(bearer)]):
    payload = jwt.decode(jwt_token)
    return JWTSchema(**payload)


async def get_user(payload: Annotated[JWTSchema, Depends(token)],
                   session: Annotated[AsyncSession, Depends(get_async_session)]) -> User:
    current_user = await UserDAO.get_by_email(email=payload.email,
                                               session=session)
    if not current_user:
        current_user = await UserDAO.create(session=session,
                                            email=payload.email)
    return (current_user if isinstance(current_user, User)
            else current_user[0] if isinstance(current_user, Sequence) and len(current_user) == 1
            else None)
