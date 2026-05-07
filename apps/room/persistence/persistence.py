from fastapi import Depends
from sqlalchemy import select
from apps.room.interfaces.interfaces import IRoomPersistence, ISeatPersistence
from apps.room.models.room import Room as RoomModel
from apps.room.models.room import Seat as SeatModel
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database import get_session
# from rabbitmq import PikaMessenger

def get_room_persistence(session: AsyncSession = Depends(get_session)):
    return RoomSqlModelPersistence(session)

def get_seat_persistence(session: AsyncSession = Depends(get_session)):
    return SeatSqlModelPersistence(session)

class RoomSqlModelPersistence(IRoomPersistence):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getAll(self):
        rooms = await self.session.scalars(
            select(RoomModel)
        )

        if not rooms:
            return []
        return rooms


    async def get(self, id: str):
        room = await self.session.scalar(
            select(RoomModel).where(RoomModel.id==id)
        )
        return room

    async def create(self, name: str, movie: str):
        room = RoomModel(
            name=name,
            movie=movie,
        )

        self.session.add(room)
        await self.session.commit()

    async def update(self, id: str, name: str, movie: str):
        room = await self.session.scalar(
            select(RoomModel).where(RoomModel.id==id)
        )
        if room:
            if name:
                room.name = name
            if movie:
                room.movie = movie
            self.session.add(room)
            await self.session.commit()


    async def delete(self, id: str):
        room = await self.session.scalar(
            select(RoomModel).where(RoomModel.id==id)
        )
        if room:
            self.session.delete(room)
            await self.session.commit()

class SeatSqlModelPersistence(ISeatPersistence):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getAll(self, room_id: int):
        seats = await self.session.scalars(
            select(SeatModel).where(SeatModel.room_id==room_id)
        )

        if not seats:
            return []
        return seats

    async def get(self, seat_id: int, room_id: int):
        seat = await self.session.scalar(
            select(SeatModel).where((SeatModel.room_id==room_id) & (SeatModel.id == seat_id))
        )
        return seat

    async def create(self, horizontal: str, vertical: str, room_id: int, user_id: int):
        seat = SeatModel(horizontal=horizontal, vertical=vertical, room_id=room_id, user_id=user_id)
        self.session.add(seat)
        await self.session.commit()

    async def update(self, seat_id: int, horizontal: str, vertical: str, room_id: int):
        seat = await self.session.scalar(
            select(SeatModel).where(SeatModel.id == seat_id)
        )

        if horizontal:
            seat.horizontal = horizontal
        if vertical:
            seat.vertical = vertical
        if room_id:
            seat.room_id = room_id

        self.session.add(seat)
        await self.session.commit()

    async def delete(self, seat_id: int):
        seat = await self.session.scalar(
            select(SeatModel).where(SeatModel.id==seat_id)
        )
        if seat:
            await self.session.delete(seat)
            await self.session.commit()

    async def set_reserved(self, seat_id: int, room_id: int):
        try:
            seat = await self.session.scalar(
                select(SeatModel)
                .where(
                    (SeatModel.room_id==room_id) & (SeatModel.id == seat_id)
                )
                .with_for_update()
            )

            if not seat or not seat.is_available:
                return False

            seat.is_available = False
            self.session.add(seat)
            await self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True


# class RoomRabbitMQPersistence(SeatSqlModelPersistence):
#     messenger = PikaMessenger()

#     def __init__(self):
#         def callback(ch, method, properties, body):
#             seat_data = json.loads(body)
#             print(seat_data)
#             if "seat_id" in seat_data and "room_id" in seat_data:
#                 persistence = SeatSqlModelPersistence()
#                 persistence.set_reserved(
#                     seat_id=seat_data["seat_id"],
#                     room_id=seat_data["room_id"],
#                 )

#         # threads
#         thread = threading.Thread(
#             target=self.messenger.consume,
#             args=(callback,)
#         )
#         thread.start()

#     def set_reserved(self, seat_id: int, room_id: int):
#         self.messenger.produce(
#             json.dumps({
#                 "seat_id": seat_id,
#                 "room_id": room_id,
#             })
#         )
#         return True
