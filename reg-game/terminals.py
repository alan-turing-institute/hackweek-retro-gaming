
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from pygame import image, Surface, transform
from random import randint

class Terminal:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location = location
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
        x = randint(0, SCREEN_WIDTH - 64)
        y = randint(0, SCREEN_HEIGHT - 64)
        terminal = Terminal(name=f"Terminal {_ + 1}", location=(x, y))
        terminals.append(terminal)
    return terminals

class TerminalView:
    def __init__(self, terminals: list[Terminal], img_path: str):
        self.terminals = terminals
        self.image = image.load(img_path)
        self.image = transform.scale(self.image, (64, 64))

    def render(self, surface: Surface):
        for terminal in self.terminals:
            if terminal.status == "active":
                surface.blit(self.image, terminal.location)
            elif terminal.status == "inactive":
                # Optionally render inactive terminals differently
                pass
            elif terminal.status == "broken":
                # Optionally render broken terminals differently
                pass