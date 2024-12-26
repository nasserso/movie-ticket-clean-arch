from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    movie: str = Field(index=True)

class Seat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    horizontal: str = Field(index=True)
    vertical: str = Field(index=True)
    is_available: bool = Field(index=True, default=True)
    room_id: int | None = Field(default=None, foreign_key="room.id")
