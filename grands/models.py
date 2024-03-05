from datetime import datetime, date, timedelta

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class Grands(Base):
    __tablename__ = "grands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    name_uz: Mapped[str] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_en: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_uz: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=(datetime.utcnow() + timedelta(hours=5)))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=(datetime.utcnow() + timedelta(hours=5)),
                                                 onupdate=(datetime.utcnow() + timedelta(hours=5)))
    image_url: Mapped[str] = mapped_column(nullable=True, comment="Image url")
    form_link: Mapped[str] = mapped_column(nullable=True, comment="Link to registration form")
    from_date: Mapped[date] = mapped_column(nullable=True, comment="grant application deadline")
    to_date: Mapped[date] = mapped_column(nullable=True, comment="grant application deadline")

    application_grands: Mapped["ApplicationGrands"] = relationship("ApplicationGrands", back_populates="grands")

    def __repr__(self):
        return f"<Grand {self.name_ru}>"
