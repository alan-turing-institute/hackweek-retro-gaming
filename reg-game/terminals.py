
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from random import randint

terminal_img = "img/CommTerminal.png" # terminal image is 32 x 32 pixels

class Terminal:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location = location
        self.image = terminal_img
        self.status = "active"

    def set_status(self, status: str):
        if status in ["active", "inactive", "broken"]:
            self.status = status
        else:
            raise ValueError("Invalid status. Must be 'active', 'inactive', or 'broken'.")

    def __repr__(self):
        return f"Terminal(name={self.name}, location={self.location})"

def create_random_terminals(num_terminals: int) -> list[Terminal]:
    terminals = []
    for _ in range(num_terminals):
        x = randint(0, SCREEN_WIDTH - 32)
        y = randint(0, SCREEN_HEIGHT - 32)
        terminal = Terminal(name=f"Terminal {_ + 1}", location=(x, y))
        terminals.append(terminal)
    return terminals