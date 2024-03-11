from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, date, time

from base.base_service import utc_now_tashkent
from config.db import Base


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_uz: Mapped[str] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    start_date: Mapped[date]
    start_time: Mapped[time]
    end_date: Mapped[date]
    end_time: Mapped[time]
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    is_paid_event: Mapped[bool]
    place: Mapped[int]
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    scores: Mapped[int]
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    image_urls: Mapped[str]
    address_uz: Mapped[str] = mapped_column(String(255), nullable=True)
    address_en: Mapped[str] = mapped_column(String(255), nullable=True)
    address_ru: Mapped[str] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_en: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_uz: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)

    # relationships
    cities: Mapped["Cities"] = relationship("Cities", back_populates="events")
    application_events: Mapped["ApplicationEvents"] = relationship("ApplicationEvents", back_populates="events")

    def __repr__(self):
        return f"<Events {self.name_ru}>"
