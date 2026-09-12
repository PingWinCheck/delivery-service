from uuid import UUID

from pydantic import BaseModel

from shop.models import ApplicationStatus


class ShopSchema(BaseModel):
    title: str
    description: str
    address: "AddressSchema"

class AddressSchema(BaseModel):
    city: str
    street: str
    home: str

class ResponseCreateShopApplication(BaseModel):
    title: str
    description: str
    status: str

class ChangeApplication(BaseModel):
    id: int
    status: ApplicationStatus
    reason: str | None = None