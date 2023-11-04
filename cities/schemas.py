from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SCityCreate(BaseModel):
    name_ru: str
    name_uz: str
    name_en: str

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
