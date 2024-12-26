from ..seat import Seat
from ..room import Room


class TestRoom:
    def test_getters(self):
        room = Room("name", "movie", "room_id")

        assert room.get_name() == "name"
        assert room.get_movie() == "movie"
        assert room.get_room_id() == "room_id"

    def test_setters(self):
        room = Room("name", "movie", "room_id")
        room.set_name("name1")
        room.set_movie("movie1")
        room.set_room_id("room_id1")

        assert room.get_name() == "name1"
        assert room.get_movie() == "movie1"
        assert room.get_room_id() == "room_id1"