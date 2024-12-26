from ..seat import Seat


class TestRoom:
    def test_getters(self):
        room = Seat("seat_id", "horizontal", "vertical", "room_id")

        assert room.get_seat_id() == "seat_id"
        assert room.get_room_id() == "room_id"
        assert room.get_horizontal() == "horizontal"
        assert room.get_vertical() == "vertical"
        assert room.get_is_available() == True

    def test_setters(self):
        room = Seat("seat_id", "horizontal", "vertical", "room_id")
        room.set_seat_id("seat_id1")
        room.set_room_id("room_id1")
        room.set_horizontal("horizontal1")
        room.set_vertical("vertical1")
        room.change_to_unavailable()

        assert room.get_seat_id() == "seat_id1"
        assert room.get_room_id() == "room_id1"
        assert room.get_horizontal() == "horizontal1"
        assert room.get_vertical() == "vertical1"
        assert room.get_is_available() == False