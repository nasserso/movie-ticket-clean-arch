from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from apps.room.interfaces.interfaces import IRoomService, ISeatService
from apps.room.routers.schemas import RoomResponseSchema, RoomSchema, SeatResponseSchema, SeatSchema
from apps.room.services.service import get_room_service, get_seat_service


router = APIRouter(prefix="/room")

@router.get("", tags=["room"], response_model=list[RoomResponseSchema])
async def get_all_rooms(roomService: IRoomService = Depends(get_room_service)):
    rooms = roomService.getAll()
    if not rooms is None:
        return rooms
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error getting rooms")

@router.get("/{room_id}", tags=["room"], response_model=RoomResponseSchema)
async def get_room(room_id: int, roomService: IRoomService = Depends(get_room_service)):
    room = roomService.get(room_id)
    if room:
        return room
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Room not found")

@router.post("", tags=["room"])
async def create_room(room: RoomSchema, roomService: IRoomService = Depends(get_room_service)):
    created = roomService.create(room.name, room.movie)
    if created:
        return Response(status_code=HTTPStatus.CREATED)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error creating room")

@router.patch("/{room_id}", tags=["room"])
async def update_room(room_id: int, room: RoomSchema, roomService: IRoomService = Depends(get_room_service)):
    updated = roomService.update(room_id, room.name, room.movie)
    if updated:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error updating room")

@router.delete("/{room_id}", tags=["room"])
async def delete_room(room_id: int, roomService: IRoomService = Depends(get_room_service)):
    deleted = roomService.delete(room_id)
    if deleted:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error deleting room")


# Seat routers

@router.get("/{room_id}/seat", tags=["seat"], response_model=list[SeatResponseSchema])
async def get_all_seats(room_id: int, seatService: ISeatService = Depends(get_seat_service)):
    seats = seatService.getAll(room_id=room_id)
    return seats

@router.get("/{room_id}/seat/{seat_id}", tags=["seat"], response_model=SeatResponseSchema)
async def get_seat(room_id: int, seat_id: int, seatService: ISeatService = Depends(get_seat_service)):
    seat = seatService.get(seat_id=seat_id, room_id=room_id)
    if seat:
        return seat
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Seat not found")

@router.post("/{room_id}/seat", tags=["seat"])
async def create_seat(seat: SeatSchema, seatService: ISeatService = Depends(get_seat_service)):
    if not seat.room_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No room id")
    if not seat.horizontal:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="No horizontal seat position")
    if not seat.vertical:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="No vertical seat position")

    created = seatService.create(seat.horizontal, seat.vertical, seat.room_id, seat.user_id)
    if created:
        return Response(status_code=HTTPStatus.CREATED)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error creating seat")

@router.patch("/{room_id}/seat/{seat_id}", tags=["seat"])
async def update_seat(seat_id: int, seat: SeatSchema, seatService: ISeatService = Depends(get_seat_service)):
    updated = seatService.update(seat_id, seat.horizontal, seat.vertical, seat.room_id)
    if updated:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error updating seat")

@router.delete("/{room_id}/seat/{seat_id}", tags=["seat"])
async def delete_seat(seat_id: int, seatService: ISeatService = Depends(get_seat_service)):
    deleted = seatService.delete(seat_id)
    if deleted:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error deleting seat")

@router.put("/{room_id}/seat/{seat_id}/reserve", tags=["seat"])
async def set_seat_reserved(seat_id: int, room_id: int, seatService: ISeatService = Depends(get_seat_service)):
    successfully_reserved = seatService.set_unavaiable(seat_id=seat_id, room_id=room_id)
    if successfully_reserved:
        return Response(status_code=HTTPStatus.OK)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error reserving seat")
