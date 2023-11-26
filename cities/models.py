from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from config.db import Base


class Cities(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    users: Mapped["Users"] = relationship(back_populates="cities")
    events: Mapped["Events"] = relationship(back_populates="cities")

    def __repr__(self):
        return f"<City {self.name_ru}>"
