class Seat:
    seat_id: str
    horizontal: str
    vertical: str
    is_available: bool = True
    room_id: str

    def __init__(self, seat_id: str, horizontal: str, vertical: str, room_id: str):
        self.seat_id = seat_id
        self.horizontal = horizontal
        self.vertical = vertical
        self.room_id = room_id

    def change_to_available(self) -> None:
        self.is_available = True

    def change_to_unavailable(self) -> None:
        self.is_available = False

    def get_seat_id(self) -> str:
        return self.seat_id
    
    def get_room_id(self) -> str:
        return self.room_id

    def get_horizontal(self) -> str:
        return self.horizontal

    def get_vertical(self) -> str:
        return self.vertical

    def get_is_available(self) -> bool:
        return self.is_available

    def set_seat_id(self, seat_id: str) -> None:
        self.seat_id = seat_id

    def set_horizontal(self, horizontal: str) -> None:
        self.horizontal = horizontal

    def set_vertical(self, vertical: str) -> None:
        self.vertical = vertical

    def set_room_id(self, room_id) -> None:
        self.room_id = room_id
