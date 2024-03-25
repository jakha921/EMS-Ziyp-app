from pydantic import BaseModel

from base.base_schema import AllOptional


class SApplicationGrandCreate(BaseModel):
    user_id: int
    grand_id: int
    status: str

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": 1,
                "grand_id": 1,
                "status": "pending"
            }
        }


class SApplicationGrandUpdate(SApplicationGrandCreate, metaclass=AllOptional):
    pass
