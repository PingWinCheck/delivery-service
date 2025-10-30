from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    username: EmailStr
    password: str
