from datetime import date

from pydantic import BaseModel, Field, validator

from base.base_schema import AllOptional


class SGrandCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_uz: str = Field(None, max_length=255)
    name_en: str = Field(None, max_length=255)
    description_ru: str = Field(None, max_length=4000)
    description_uz: str = Field(None, max_length=4000)
    description_en: str = Field(None, max_length=4000)
    image_url: list = Field(None)
    form_link: str = Field(None, max_length=255)
    from_date: date = Field(None)
    to_date: date = Field(None)

    # validate from and to date
    @validator('from_date')
    def from_date_must_be_less_than_to_date(cls, v, values):
        if 'to_date' in values and v > values['to_date']:
            raise ValueError('from_date must be less than to_date')
        return v

    @validator('to_date')
    def to_date_must_be_greater_than_from_date(cls, v, values):
        if 'from_date' in values and v < values['from_date']:
            raise ValueError('to_date must be greater than from_date')
        return v

    @validator('from_date', 'to_date')
    def date_must_be_greater_than_today(cls, v):
        if v < date.today():
            raise ValueError('date must be greater than today')
        return v

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Название",
                "name_uz": "Nomi",
                "name_en": "Name",
                "description_ru": "Описание",
                "description_uz": "Tavsif",
                "description_en": "Description",
                "image_url": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ],
                "form_link": "https://someurl.com",
                "from_date": "2021-01-01",
                "to_date": "2021-01-01"
            }
        }


class SGrandUpdate(SGrandCreate, metaclass=AllOptional):
    pass
