from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SCityCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_uz: str = Field(None, max_length=255)
    name_en: str = Field(None, max_length=255)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Ташкент",
                "name_uz": "Toshkent",
                "name_en": "Tashkent"
            }
        }


class SCityUpdate(SCityCreate, metaclass=AllOptional):
    pass
