from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from shop.models import ApplicationStatus

class ShopBaseSchema(BaseModel):
    title: str
    description: str


class ShopCrateSchema(ShopBaseSchema):
    address: "AddressSchema"

class AddressSchema(BaseModel):
    city: str
    street: str
    home: str

class ResponseCreateShopApplicationSchema(ShopBaseSchema):
    status: str

class ChangeApplication(BaseModel):
    id: int
    status: ApplicationStatus
    reason: str | None = None

class ShopSchema(ShopBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: UUID
    address_id: int
    status: ApplicationStatus
    reviewed_at: datetime | None = None
    reviewed_by_id: UUID | None = None
    reason: str | None = None

class ShopHistorySchema(ShopSchema):
    shop_id: int

class ApplicationResponseSchema(BaseModel):
    shop: ShopSchema
    shop_history: list[ShopHistorySchema] | None = None

