from abc import ABC, abstractmethod

from apps.room.entities.room import Room
from apps.room.entities.seat import Seat

class IRoomService(ABC):
    @abstractmethod
    def get(id: int) -> Room:
        raise NotImplementedError

    @abstractmethod
    def create(name: str, movie: str) -> Room:
        raise NotImplementedError

    @abstractmethod
    def update(id: int, name: str, movie: str) -> Room:
        raise NotImplementedError

    @abstractmethod
    def delete(id: int) -> Room:
        raise NotImplementedError

class IRoomPersistence(ABC):
    @abstractmethod
    def getAll():
        raise NotImplementedError

    @abstractmethod
    def get(id: int):
        raise NotImplementedError

    @abstractmethod
    def create(name: str, movie: str):
        raise NotImplementedError

    @abstractmethod
    def update(id: int, name: str, movie: str):
        raise NotImplementedError

    @abstractmethod
    def delete(id: int):
        raise NotImplementedError


class ISeatService(ABC):
    @abstractmethod
    def get(seat_id: int) -> Seat:
        raise NotImplementedError

    @abstractmethod
    def create(horizontal: str, vertical: str, room_id: int) -> Seat:
        raise NotImplementedError

    @abstractmethod
    def update(seat_id: int, horizontal: str, vertical: str, room_id: int) -> Seat:
        raise NotImplementedError

    @abstractmethod
    def delete(seat_id: int) -> Seat:
        raise NotImplementedError

class ISeatPersistence(ABC):
    @abstractmethod
    def getAll():
        raise NotImplementedError

    @abstractmethod
    def get(seat_id: int):
        raise NotImplementedError

    @abstractmethod
    def create(horizontal: str, vertical: str, room_id: int):
        raise NotImplementedError

    @abstractmethod
    def update(seat_id: int, horizontal: str|None, vertical: str|None, room_id: int|None):
        raise NotImplementedError

    @abstractmethod
    def delete(seat_id: int):
        raise NotImplementedError

    @abstractmethod
    def delete(seat_id: int, room_id: int):
        raise NotImplementedError