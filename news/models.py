from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
import pytz

from config.db import Base

tashkent = pytz.timezone('Asia/Tashkent')


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_uz: Mapped[str] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_en: Mapped[str] = mapped_column(String(4000), nullable=True)
    description_uz: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(tashkent))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(tashkent),
                                                 onupdate=datetime.now(tashkent))
    images: Mapped[str] = mapped_column(nullable=True, comment="Array of image urls")

    def __repr__(self):
        return f"<News {self.name_ru}>"
