from pydantic import BaseModel, Field


class SVolunteerCreate(BaseModel):
    user_id: int = Field(..., example="1")

    class Config:
        orm_mode = True
