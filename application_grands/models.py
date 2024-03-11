from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from base.base_service import utc_now_tashkent


class ApplicationGrands(Base):
    __tablename__ = "application_grands"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    grand_id: Mapped[int] = mapped_column(ForeignKey("grands.id"), nullable=False)
    status: Mapped[str] = mapped_column(Enum("pending", "approved", "rejected", name="status"), nullable=False,
                                        default="pending")
    description: Mapped[str] = mapped_column(String(4000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)

    users: Mapped["Users"] = relationship("Users", back_populates="application_grands")
    grands: Mapped["Grands"] = relationship("Grands", back_populates="application_grands")

    def __repr__(self):
        return f"<ApplicationGrand {self.user_id} - {self.status}>"
