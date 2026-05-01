from sqlalchemy.orm import Session

from apps.room.models.room import Room, Seat
from apps.room.persistence.persistence import SeatSqlModelPersistence  


def test_set_unavailable_idempotent(client, session: Session):
    room = Room(
        name="test_room",
        movie="test_movie",
    )
    session.add(room)
    session.commit()
    session.refresh(room)

    seat = Seat(
        horizontal="h",
        vertical="1",
        room_id=room.id,
    )
    session.add(seat)
    session.commit()
    session.refresh(seat)

    result_ok = SeatSqlModelPersistence(session=session).set_unavaiable(
        seat_id=seat.id,
        room_id=room.id
    )
    result_error = SeatSqlModelPersistence(session=session).set_unavaiable(
        seat_id=seat.id,
        room_id=room.id
    )

    assert result_ok
    assert not result_error
