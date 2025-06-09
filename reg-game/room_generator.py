
from enum import Enum
class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

class Background:
    def __init__(self, image_path):
        self.image_path = image_path

    def __str__(self):
        return f"Background(image_path={self.image_path})"

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.background = None

    def set_exit(self, direction: Direction, room):
        self.exits[direction] = room

    def get_exit(self, direction):
        return self.exits.get(direction)

    def set_background(self, background):
        self.background = background

    def __str__(self):
        return f"{self.name}: {self.description}"

def generate_map(n_rooms):
    rooms = []
    for i in range(n_rooms):
        name = f"Room {i + 1}"
        description = f"This is the description of {name}."
        room = Room(name, description)
        room.set_background("img/player_spritesheet.png")
        rooms.append(room)

    # Set exits between rooms
    for i in range(n_rooms - 1):
        rooms[i].set_exit(Direction.NORTH, rooms[i + 1])
        rooms[i + 1].set_exit(Direction.SOUTH, rooms[i])

    return rooms

