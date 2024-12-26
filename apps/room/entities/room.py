class Room:
    room_id: str
    name: str
    movie: str

    def __init__(self, name: str, movie: str, room_id: str):
        self.name = name
        self.movie = movie
        self.room_id = room_id

    def get_name(self) -> str:
        return self.name

    def get_movie(self) -> str:
        return self.movie
    
    def get_room_id(self) -> str:
        return self.room_id

    def set_name(self, name: str) -> str:
        self.name = name

    def set_movie(self, movie: str) -> str:
        self.movie = movie

    def set_room_id(self, room_id: str) -> str:
        self.room_id = room_id
