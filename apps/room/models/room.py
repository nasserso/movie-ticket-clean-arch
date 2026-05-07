# from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "pk": "pk_%(table_name)s",
}

table_registry.metadata.naming_convention = convention


@table_registry.mapped_as_dataclass
class Room:
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    movie: Mapped[str]
    seats: Mapped[list[Seat]] = relationship(
        init=False,
        cascade="all, delete-orphan",
        lazy='selectin',
    )


@table_registry.mapped_as_dataclass
class Seat:
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    horizontal: Mapped[str]
    vertical: Mapped[str]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(init=False, back_populates="seat", single_parent=True)
    is_available: bool = mapped_column(default=True)

    __table_args__ = (
        UniqueConstraint("horizontal", "vertical", "room_id", name="uq_seat_position"),
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    seat: Mapped["Seat"] = relationship(back_populates="user")
