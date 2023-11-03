from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Volunteers(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[int] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[int] = mapped_column(default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return f"<Volunteer {self.id}>"