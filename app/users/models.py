from datetime import date, datetime

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.base_service import utc_now_tashkent
from config.db import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    role: Mapped[str] = mapped_column(Enum("admin", "user", "master", name="role"), nullable=False,
                                      comment="Static 3 roles as user, admin and master")
    dob: Mapped[date] = mapped_column(nullable=True)
    study_in: Mapped[str] = mapped_column(String(255), nullable=True, comment="Need to add where user is study")
    work_in: Mapped[str] = mapped_column(String(255), nullable=True, comment="Need to add where user is work")
    additional_data: Mapped[str] = mapped_column(String(4000), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    balance: Mapped[int] = mapped_column(nullable=True, default=0)
    device_token: Mapped[str] = mapped_column(String(255), nullable=True,
                                              comment="Device token for push notifications used by firebase")
    # set time for created_at and updated_at columns +5 hours
    registered_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now_tashkent,
                                                 onupdate=utc_now_tashkent)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
    is_completed_profile: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                       comment="If user completed profile or not")
    is_volunteer: Mapped[bool] = mapped_column(nullable=True, default=False, comment="If user is volunteer or not")
    lang: Mapped[str] = mapped_column(String(2), nullable=True, default="ru", comment="Language of user")

    # relationships
    cities: Mapped["Cities"] = relationship("Cities", back_populates="users")

    volunteers: Mapped["Volunteers"] = relationship("Volunteers", back_populates="users")
    orders: Mapped["Orders"] = relationship("Orders", back_populates="users")
    application_events: Mapped["ApplicationEvents"] = relationship("ApplicationEvents", back_populates="users")
    application_grands: Mapped["ApplicationGrands"] = relationship("ApplicationGrands", back_populates="users")

    def __repr__(self):
        return f"<User {self.phone or self.email}>"
