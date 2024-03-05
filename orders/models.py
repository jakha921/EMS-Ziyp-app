from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timedelta

from config.db import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=(datetime.utcnow() + timedelta(hours=5)))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=(datetime.utcnow() + timedelta(hours=5)),
                                                 onupdate=(datetime.utcnow() + timedelta(hours=5)))

    # check for uniqueness
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )

    users: Mapped["Users"] = relationship("Users", back_populates="orders")
    products: Mapped["Products"] = relationship("Products", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"
