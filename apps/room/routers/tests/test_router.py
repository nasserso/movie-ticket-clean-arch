from http import HTTPStatus

from sqlalchemy.orm import Session

from apps.room.models.room import Room, Seat  

def test_set_unavailable(client, session: Session):
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

    response_ok = client.put(f'/room/{room.id}/seat/{seat.id}/reserve')
    assert response_ok.status_code == HTTPStatus.OK

    response_conflict = client.put(f'/room/{room.id}/seat/{seat.id}/reserve')
    assert response_conflict.status_code == HTTPStatus.BAD_REQUEST
    assert response_conflict.json() == {'detail': 'Error reserving seat'}  
