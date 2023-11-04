from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SCategoryCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_en: str = Field(max_length=255)
    name_uz: str = Field(max_length=255)
    description: str = Field(None, max_length=4000)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Категория",
                "name_en": "Category",
                "name_uz": "Kategoriya",
                "description": "Описание категории"
            }
        }


class SCategoryUpdate(SCategoryCreate, metaclass=AllOptional):
    pass
