from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response

from apps.room.persistence.persistence import RoomSqlModelPersistence, SeatSqlModelPersistence
from apps.room.routers.schemas import RoomResponseSchema, RoomSchema, SeatSchema
from apps.room.services.service import RoomService, SeatService


router = APIRouter(prefix="/room")

roomPersistence = RoomSqlModelPersistence()
roomService = RoomService(roomPersistence)

@router.get("", tags=["room"], response_model=list[RoomResponseSchema])
async def get_all_rooms():
    rooms = roomService.getAll()
    return rooms

@router.get("/{room_id}", tags=["room"], response_model=RoomResponseSchema)
async def get_room(room_id: int):
    room = roomService.get(room_id)
    if room:
        return room
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Room not found")

@router.post("", tags=["room"])
async def create_room(room: RoomSchema):
    created = roomService.create(room.name, room.movie)
    if created:
        return Response(status_code=HTTPStatus.CREATED)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error creating room")

@router.patch("/{room_id}", tags=["room"])
async def update_room(room_id: int, room: RoomSchema):
    updated = roomService.update(room_id, room.name, room.movie)
    if updated:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error updating room")

@router.delete("/{room_id}", tags=["room"])
async def delete_room(room_id: int):
    deleted = roomService.delete(room_id)
    if deleted:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error deleting room")


# Seat routers
seatPersistence = SeatSqlModelPersistence()
# seatPersistence = RoomRabbitMQPersistence()
seatService = SeatService(seatPersistence)

@router.get("/{room_id}/seat", tags=["seat"], response_model=list[SeatSchema])
async def get_all_seats(room_id: int):
    seats = seatService.getAll(room_id=room_id)
    return seats

@router.get("/{room_id}/seat/{seat_id}", tags=["seat"], response_model=SeatSchema)
async def get_seat(room_id: int, seat_id: int):
    seat = seatService.get(seat_id=seat_id, room_id=room_id)
    if seat:
        return seat
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Seat not found")

@router.post("/{room_id}/seat", tags=["seat"])
async def create_seat(seat: SeatSchema):
    if not seat.room_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No room id")
    if not seat.horizontal:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No horizontal seat position")
    if not seat.vertical:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No vertical seat position")

    created = seatService.create(seat.horizontal, seat.vertical, seat.room_id)
    if created:
        return Response(status_code=HTTPStatus.CREATED)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error creating seat")

@router.patch("/{room_id}/seat/{seat_id}", tags=["seat"])
async def update_seat(seat_id: int, seat: SeatSchema):
    updated = seatService.update(seat_id, seat.horizontal, seat.vertical, seat.room_id)
    if updated:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error updating seat")

@router.delete("/{room_id}/seat/{seat_id}", tags=["seat"])
async def delete_seat(seat_id: int):
    deleted = seatService.delete(seat_id)
    if deleted:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error deleting seat")

@router.post("/{room_id}/seat/{seat_id}", tags=["seat"])
async def set_seat_occupied(seat_id: int, room_id: int):
    successfully_occupied = seatService.set_unavaiable(seat_id=seat_id, room_id=room_id)
    if successfully_occupied:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error occupying seat")
