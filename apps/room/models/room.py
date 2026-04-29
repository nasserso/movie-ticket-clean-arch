from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


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
    is_available: bool = mapped_column(default=True)

