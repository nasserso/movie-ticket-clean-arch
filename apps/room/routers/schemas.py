from pydantic import BaseModel

class RoomResponseSchema(BaseModel):
    id: int
    name: str
    movie: str

class RoomSchema(BaseModel):
    name: str
    movie: str

