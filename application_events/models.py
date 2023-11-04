from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class ApplicationEvents(Base):
    __tablename__ = "application_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    status: Mapped[str] = mapped_column(Enum("pending", "approved", "rejected", name="status"), nullable=False,
                                        default="pending")
    description: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    users: Mapped["Users"] = relationship("Users", back_populates="application_events")
    events: Mapped["Events"] = relationship("Events", back_populates="application_events")

    def __repr__(self):
        return f"<ApplicationEvent {self.event_id} - {self.user_id} - {self.status}>"
