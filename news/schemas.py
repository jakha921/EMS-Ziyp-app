from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SNewsCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_uz: str = Field(None, max_length=255)
    name_en: str = Field(None, max_length=255)
    description_ru: str = Field(None, max_length=4000)
    description_uz: str = Field(None, max_length=4000)
    description_en: str = Field(None, max_length=4000)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Название",
                "name_uz": "Nomi",
                "name_en": "Name",
                "description_ru": "Описание",
                "description_uz": "Tavsif",
                "description_en": "Description"
            }
        }


class SNewsUpdate(SNewsCreate, metaclass=AllOptional):
    pass
