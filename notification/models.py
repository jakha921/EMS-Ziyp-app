from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from base.base_service import utc_now_tashkent
from config.db import Base


class Notifications(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    title_ru: Mapped[str] = mapped_column(String(255))
    title_uz: Mapped[str] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str] = mapped_column(String(255), nullable=True)
    body_ru: Mapped[str] = mapped_column(String(4000), nullable=True)
    body_en: Mapped[str] = mapped_column(String(4000), nullable=True)
    body_uz: Mapped[str] = mapped_column(String(4000), nullable=True)
    datetime_to_send: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)

    # relationships
    events: Mapped["Events"] = relationship("Events", back_populates="notifications")

    def __repr__(self):
        return f"<Notifications {self.title_ru}>"
