from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, date, time

from config.db import Base


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_uz: Mapped[str] = mapped_column(String(255))
    name_en: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[date]
    start_time: Mapped[time]
    end_date: Mapped[date]
    end_time: Mapped[time]
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    is_paid_event: Mapped[bool]
    place: Mapped[int]
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    scores: Mapped[int]
    image_urls: Mapped[str]
    description_ru: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_en: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_uz: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    # cities: Mapped["Cities"] = relationship("Cities", back_populates="events")
    # application_events = relationship("ApplicationEvents", back_populates="events")

    def __repr__(self):
        return f"<Events {self.name_ru}>"
