from typing import List
from apps.room.entities.room import Room
from apps.room.entities.seat import Seat
from apps.room.interfaces.interfaces import IRoomPersistence, IRoomService, ISeatPersistence, ISeatService

class RoomService(IRoomService):
    persistence: IRoomPersistence

    def __init__(self, persistence: IRoomPersistence):
        self.persistence = persistence

    def getAll(self) -> List[Room]:
        roomList = self.persistence.getAll()
        # TODO: map to room obj
        return list(map(lambda r: { "id": r.id, "name": r.name, "movie": r.movie }, roomList))

    def get(self, id: str) -> Room | bool:
        room = self.persistence.get(id)
        # TODO: map to room obj
        if room:
            return { "id": room.id, "name": room.name, "movie": room.movie }

    def create(self, name: str, movie: str) -> bool:
        room = Room(name=name, movie=movie, room_id="")
        self.persistence.create(room.get_name(), room.get_movie())
        return True

    def update(self, id: str, name: str, movie: str) -> bool:
        self.persistence.update(id, name, movie)
        return True

    def delete(self, id: str) -> bool:
        self.persistence.delete(id)
        return True

class SeatService(ISeatService):
    persistence: ISeatPersistence

    def __init__(self, persistence: ISeatPersistence):
        self.persistence = persistence

    def getAll(self, room_id: int) -> List[Seat]:
        seatList = self.persistence.getAll(room_id)
        # TODO: map to seat obj
        return list(map(lambda s: { 
            "seat_id": s.id,
            "horizontal": s.horizontal,
            "vertical": s.vertical,
            "is_available": s.is_available,
            "room_id": s.room_id,
        }, seatList))

    def get(self, seat_id: int, room_id: int) -> Seat | bool:
        seat = self.persistence.get(seat_id, room_id)
        # TODO: map to seat obj
        if seat:
            return {
            "seat_id": seat.id,
            "horizontal": seat.horizontal,
            "vertical": seat.vertical,
            "is_available": seat.is_available,
            "room_id": seat.room_id,
        }

    def create(self, horizontal: str, vertical: str, room_id: int) -> bool:
        seat = Seat(horizontal=horizontal, vertical=vertical, seat_id="", room_id=room_id)
        self.persistence.create(seat.get_horizontal(), seat.get_vertical(), seat.get_room_id())
        return True

    def update(self, seat_id: int, horizontal: str, vertical: str, room_id: int) -> bool:
        self.persistence.update(seat_id, horizontal, vertical, room_id)
        return True

    def delete(self, seat_id: int) -> bool:
        self.persistence.delete(seat_id)
        return True
    
    def set_unavaiable(self, seat_id: int, room_id: int):
        successfully_occupied = self.persistence.set_unavaiable(seat_id=seat_id, room_id=room_id)
        return successfully_occupied
