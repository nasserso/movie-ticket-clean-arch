import json
from apps.room.interfaces.interfaces import IRoomPersistence, ISeatPersistence
from sqlmodel import select
from sqlmodel import Session
from apps.room.models.room import Room as RoomModel
from apps.room.models.room import Seat as SeatModel

from database import engine
from rabbitmq import PikaMessenger

import threading

class RoomSqlModelPersistence(IRoomPersistence):
    def getAll(self):
        with Session(engine) as session:
            session = Session(engine)
            statement = select(RoomModel)
            results = session.exec(statement)
            rooms = results.all()
            return rooms

    def get(self, id: str):
        with Session(engine) as session:
            session = Session(engine)
            room = session.get(RoomModel, id)
            return room

    def create(self, name: str, movie: str):
        room = RoomModel(name=name, movie=movie)

        with Session(engine) as session:
            session.add(room)
            session.commit()

    def update(self, id: str, name: str, movie: str):
        with Session(engine) as session:
            session = Session(engine)
            room = session.get(RoomModel, id)
            if name:
                room.name = name
            if movie:
                room.movie = movie
            session.add(room)
            session.commit()

    def delete(self, id: str):
        with Session(engine) as session:
            session = Session(engine)
            room = session.get(RoomModel, id)
            session.delete(room)
            session.commit()

class SeatSqlModelPersistence(ISeatPersistence):
    def getAll(self, room_id: int):
        with Session(engine) as session:
            session = Session(engine)
            statement = select(SeatModel).where(SeatModel.room_id == room_id)
            results = session.exec(statement)
            seats = results.all()
            return seats

    def get(self, seat_id: int, room_id: int):
        with Session(engine) as session:
            session = Session(engine)
            statement = select(SeatModel).where(SeatModel.room_id == room_id).where(SeatModel.id == seat_id)
            results = session.exec(statement)
            seats = results.first()
            return seats

    def create(self, horizontal: str, vertical: str, room_id: int):
        seat = SeatModel(horizontal=horizontal, vertical=vertical, room_id=room_id)

        with Session(engine) as session:
            session.add(seat)
            session.commit()

    def update(self, seat_id: int, horizontal: str, vertical: str, room_id: int):
        with Session(engine) as session:
            session = Session(engine)
            seat = session.get(SeatModel, seat_id)

            if horizontal:
                seat.horizontal = horizontal
            if vertical:
                seat.vertical = vertical
            if room_id:
                seat.room_id = room_id

            session.add(seat)
            session.commit()

    def delete(self, seat_id: int):
        with Session(engine) as session:
            session = Session(engine)
            seat = session.get(SeatModel, seat_id)
            session.delete(seat)
            session.commit()

    def set_unavaiable(self, seat_id: int, room_id: int):
        with Session(engine) as session:
            session = Session(engine)
            seat = session.get(SeatModel, seat_id)

            if seat.is_available == False:
                return False
            else:
                seat.is_available = False
                session.add(seat)
                session.commit()
        return True

class RoomRabbitMQPersistence(SeatSqlModelPersistence):
    messenger = PikaMessenger()

    def __init__(self):
        def callback(ch, method, properties, body):
            seat_data = json.loads(body)
            print(seat_data)
            if "seat_id" in seat_data and "room_id" in seat_data:
                persistence = SeatSqlModelPersistence()
                persistence.set_unavaiable(
                    seat_id=seat_data["seat_id"],
                    room_id=seat_data["room_id"],
                )

        # threads
        thread = threading.Thread(
            target=self.messenger.consume,
            args=(callback,)
        )
        thread.start()

    def set_unavaiable(self, seat_id: int, room_id: int):
        self.messenger.produce(
            json.dumps({
                "seat_id": seat_id,
                "room_id": room_id,
            })
        )
        return True
