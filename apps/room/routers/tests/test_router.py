from http import HTTPStatus
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from apps.room.models.room import Room, Seat  

@pytest.mark.asyncio
async def test_set_reserved(client, session: AsyncSession):
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

    response_ok = client.put(f'/room/{room.id}/seat/{seat.id}/reserve')
    assert response_ok.status_code == HTTPStatus.OK

    response_conflict = client.put(f'/room/{room.id}/seat/{seat.id}/reserve')
    assert response_conflict.status_code == HTTPStatus.BAD_REQUEST
    assert response_conflict.json() == {'detail': 'Error reserving seat'}  
