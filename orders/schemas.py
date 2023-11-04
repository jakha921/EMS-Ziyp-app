from pydantic import BaseModel, Field


class SOrderCreate(BaseModel):
    user_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
