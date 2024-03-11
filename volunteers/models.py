from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.base_service import utc_now_tashkent
from config.db import Base


class Volunteers(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)

    # relationships
    users: Mapped["Users"] = relationship("Users", back_populates="volunteers")

    def __repr__(self):
        return f"<Volunteer {self.id}>"
