import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from apps.room.models.room import Room, Seat
from apps.room.persistence.persistence import SeatSqlModelPersistence  


@pytest.mark.asyncio
async def test_set_reserved_idempotent(client, session: AsyncSession):
    room = Room(
        name="test_room",
        movie="test_movie",
    )
    session.add(room)
    await session.commit()
    await session.refresh(room)

    seat = Seat(
        horizontal="h",
        vertical="1",
        room_id=room.id,
        user_id=1,
    )
    session.add(seat)
    await session.commit()
    await session.refresh(seat)

    result_ok = await SeatSqlModelPersistence(session=session).set_reserved(
        seat_id=seat.id,
        room_id=room.id
    )
    result_error = await SeatSqlModelPersistence(session=session).set_reserved(
        seat_id=seat.id,
        room_id=room.id
    )

    assert result_ok
    assert not result_error
