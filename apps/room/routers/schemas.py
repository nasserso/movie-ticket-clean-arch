from pydantic import BaseModel

class RoomResponseSchema(BaseModel):
    id: int
    name: str
    movie: str

class RoomSchema(BaseModel):
    name: str
    movie: str

class SeatSchema(BaseModel):
    horizontal: str
    vertical: str
    room_id: int
    user_id: int

class SeatResponseSchema(SeatSchema):
    horizontal: str
    vertical: str
    room_id: int
    is_available: bool
