from typing import List
from apps.room.entities.room import Room
from apps.room.entities.seat import Seat
from apps.room.interfaces.interfaces import IRoomPersistence, IRoomService, ISeatPersistence, ISeatService

class RoomService(IRoomService):
    persistence: IRoomPersistence

    def __init__(self, persistence: IRoomPersistence):
        self.persistence = persistence

    def getAll(self) -> List[Room]:
        try:
            roomList = self.persistence.getAll()
            return roomList
        except Exception as e:
            print(e)

    def get(self, id: str) -> Room | bool:
        try:
            room = self.persistence.get(id)
            return room
        except Exception as e:
            print(e)

    def create(self, name: str, movie: str) -> bool:
        try:
            room = Room(name=name, movie=movie, room_id="")
            self.persistence.create(room.get_name(), room.get_movie())
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, id: str, name: str, movie: str) -> bool:
        try:
            self.persistence.update(id, name, movie)
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, id: str) -> bool:
        try:
            self.persistence.delete(id)
            return True
        except Exception as e:
            print(e)
            return False

class SeatService(ISeatService):
    persistence: ISeatPersistence

    def __init__(self, persistence: ISeatPersistence):
        self.persistence = persistence

    def getAll(self, room_id: int) -> List[Seat]:
        try:
            seatList = self.persistence.getAll(room_id)
            return seatList
        except Exception as e:
            print(e)


    def get(self, seat_id: int, room_id: int) -> Seat | bool:
        try:
            seat = self.persistence.get(seat_id, room_id)
            if seat:
                return seat
        except Exception as e:
            print(e)

    def create(self, horizontal: str, vertical: str, room_id: int) -> bool:
        try:
            seat = Seat(horizontal=horizontal, vertical=vertical, seat_id="", room_id=room_id)
            self.persistence.create(seat.get_horizontal(), seat.get_vertical(), seat.get_room_id())
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, seat_id: int, horizontal: str, vertical: str, room_id: int) -> bool:
        try:
            self.persistence.update(seat_id, horizontal, vertical, room_id)
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, seat_id: int) -> bool:
        try:
            self.persistence.delete(seat_id)
            return True
        except Exception as e:
            print(e)
            return False
    
    def set_unavaiable(self, seat_id: int, room_id: int):
        try:
            successfully_occupied = self.persistence.set_unavaiable(seat_id=seat_id, room_id=room_id)
            return successfully_occupied
        except Exception as e:
            print(e)
            return False
    