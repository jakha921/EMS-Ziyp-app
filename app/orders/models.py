from datetime import datetime

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.base_service import utc_now_tashkent
from config.db import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)

    # Create Enum type in database (create_type=True ensures enum is created)
    order_status: Mapped[str] = mapped_column(
        Enum("new", "in_progress", "completed", "canceled", "ready",
             name="order_status"), nullable=True, default="new")
    count: Mapped[int] = mapped_column(nullable=True, default=0)

    users: Mapped["Users"] = relationship("Users", back_populates="orders")
    products: Mapped["Products"] = relationship("Products", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"
