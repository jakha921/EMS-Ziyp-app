from datetime import date

from pydantic import BaseModel, EmailStr, Field


class SAdminRegister(BaseModel):
    email: EmailStr = Field(..., example="admin@gmail.com")
    password: str = Field(..., example="12345678")


class SAdminAuth(SAdminRegister):
    pass


class SMasterRester(BaseModel):
    last_name: str = Field(..., example="Doe")
    first_name: str = Field(..., example="John")
    phone: str = Field(..., example="+998901234567")
    password: str = Field(..., example="12345678")


class SMasterUpdate(BaseModel):
    pass


class SUserRegister(BaseModel):
    phone: str = Field(..., example="+998901234567")
    password: str = Field(..., example="12345678")


class SUserAuth(SUserRegister):
    pass


class SUserUpdate(BaseModel):
    phone: str = Field(None, example="+998901234567")
    password: str = Field(None, example="12345678")
    first_name: str = Field(None, example="John")
    last_name: str = Field(None, example="Doe")
    middle_name: str = Field(None, example="Doe")
    email: EmailStr = Field(None, example="john@doe.com")
    city_id: int = Field(None, example=1)
    dob: date = Field(None, example="1990-01-01")
    study_in: str = Field(None, example="TUIT")
    work_in: str = Field(None, example="TUIT")
    additional_data: str = Field(None, example="Some additional data")
    avatar_url: list = Field(None, example=["https://example.com/1.jpg", "https://example.com/2.jpg"])
    balance: int = Field(None, example=1000)

    class Config:
        orm_mode = True
