from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class Volunteers(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow(), onupdate=datetime.utcnow())

    # relationships
    users: Mapped["Users"] = relationship("Users", back_populates="volunteers")

    def __repr__(self):
        return f"<Volunteer {self.id}>"
