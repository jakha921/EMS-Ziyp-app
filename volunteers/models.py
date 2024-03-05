from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class Volunteers(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=(datetime.utcnow() + timedelta(hours=5)))
    updated_at: Mapped[datetime] = mapped_column(default=(datetime.utcnow() + timedelta(hours=5)),
                                                 onupdate=(datetime.utcnow() + timedelta(hours=5)))

    # relationships
    users: Mapped["Users"] = relationship("Users", back_populates="volunteers")

    def __repr__(self):
        return f"<Volunteer {self.id}>"
