from datetime import date, time

from pydantic import BaseModel, Field

from base.base_schema import AllOptional


class SEventCreate(BaseModel):
    name_ru: str = Field(max_length=255)
    name_uz: str = Field(None, max_length=255)
    name_en: str = Field(None, max_length=255)
    start_date: date
    start_time: time
    end_date: date
    end_time: time
    city_id: int
    place: int
    is_paid_event: bool
    price: int
    scores: int
    address_ru: str = Field(None, max_length=255)
    address_uz: str = Field(None, max_length=255)
    address_en: str = Field(None, max_length=255)
    description_ru: str = Field(None, max_length=4000)
    description_uz: str = Field(None, max_length=4000)
    description_en: str = Field(None, max_length=4000)
    image_urls: list = Field(None)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name_ru": "Event name",
                "name_uz": "Event name",
                "name_en": "Event name",
                "start_date": "2021-01-01",
                "start_time": "00:00:00",
                "end_date": "2021-01-01",
                "end_time": "00:00:00",
                "city_id": 1,
                "place": 1,
                "is_paid_event": True,
                "price": 10000,
                "scores": 10,
                "address_ru": "Event address",
                "address_uz": "Event address",
                "address_en": "Event address",
                "description_ru": "Event description",
                "description_uz": "Event description",
                "description_en": "Event description",
                "image_urls": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ]
            }
        }


class SEventUpdate(SEventCreate, metaclass=AllOptional):
    pass
