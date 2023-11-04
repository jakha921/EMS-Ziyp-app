from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SProductCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_uz: str = Field(max_length=255)
    name_en: str = Field(max_length=255)
    price: int
    description_ru: str = Field(max_length=4000)
    description_uz: str = Field(max_length=4000)
    description_en: str = Field(max_length=4000)
    category_id: int
    images: list = Field(None)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Продукт",
                "name_uz": "Mahsulot",
                "name_en": "Product",
                "price": 1000,
                "description_ru": "Описание продукта",
                "description_uz": "Mahsulot haqida",
                "description_en": "Product description",
                "category_id": 1,
                "images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ]
            }
        }


class SProductUpdate(SProductCreate, metaclass=AllOptional):
    pass
