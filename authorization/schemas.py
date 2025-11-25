from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    username: EmailStr
    password: str


class JWTSchema(BaseModel):
    sub: UUID
    email: EmailStr