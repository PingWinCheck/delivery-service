from pydantic import BaseModel,Field
from fastapi import Query

class PagerInputSchema(BaseModel):
    page: int = 1
    size: int = Field(default=20, le=70)

class PagerOutputSchema(BaseModel):
    limit: int
    offset: int

class MetaForPageSchema(BaseModel):
    total: int

class ResponseForPageSchema[DataT](BaseModel):
    data: DataT
    meta: MetaForPageSchema