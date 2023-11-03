from pydantic import BaseModel, EmailStr, Field


class SAdminRegister(BaseModel):
    email: EmailStr = Field(..., example="admin@gmail.com")
    password: str = Field(..., example="12345678")


class SAdminAuth(SAdminRegister):
    pass


class SUserRegister(BaseModel):
    phone: str = Field(..., example="+998901234567")
    password: str = Field(..., example="12345678")


class SUserAuth(SUserRegister):
    pass
