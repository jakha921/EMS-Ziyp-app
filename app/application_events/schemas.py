from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SApplicationEventCreate(BaseModel):
    user_id: int
    event_id: int
    status: str

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": 1,
                "event_id": 1,
                "status": "pending"
            }
        }


class SSApplicationEventUpdate(SApplicationEventCreate, metaclass=AllOptional):
    pass
