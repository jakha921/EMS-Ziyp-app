from enum import Enum

from pydantic import BaseModel, Field


class SOrderCreate(BaseModel):
    user_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    order_status: str = Field(..., example="new")
    count: int = Field(..., example=0)


class SOrderUpdate(SOrderCreate):
    user_id: int = Field(None, example=1)
    product_id: int = Field(None, example=1)
    order_status: str = Field(None, example="new")
    count: int = Field(None, example=0)
