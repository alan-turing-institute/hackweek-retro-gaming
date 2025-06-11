from random import randint

from config import SCREEN_HEIGHT, SCREEN_WIDTH
from pygame import Surface, image
from framework import StateMachine, State


class ActiveState(State):

    def __init__(self):
        super().__init__("active")


class HackingState(State):
    def __init__(self):
        super().__init__("hacking")


class FixingState(State):
    def __init__(self):
        super().__init__("fixing")


class BrokenState(State):
    def __init__(self):
        super().__init__("broken")


class TerminalModel:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location: tuple[int, int] = location
        self.state_machine = StateMachine()
        self.state_machine.add_state(ActiveState())
        self.state_machine.add_state(HackingState())
        self.state_machine.add_state(FixingState())
        self.state_machine.add_state(BrokenState())

        self.state_machine.set_state("active")

    def set_status(self, status: str):
        if status in ["active", "inactive", "broken", "hacking"]:
            self.status = status
        else:
            raise ValueError(
                "Invalid status. Must be 'active', 'inactive', 'broken', or 'hacking'."
            )

    def __repr__(self):
        return f"Terminal(name={self.name}, location={self.location})"


class TerminalController:

    def __init__(self, number_of_terminals: int) -> None:
        self.terminals: list[TerminalModel] = []
        self.create_random_terminals(number_of_terminals)

    def create_random_terminals(self, num_terminals: int):
        for _ in range(num_terminals):
            x = randint(0, SCREEN_WIDTH - 32)
            y = randint(0, SCREEN_HEIGHT - 32)
            terminal = TerminalModel(name=f"Terminal {_ + 1}", location=(x, y))
            self.terminals.append(terminal)

    def update(self, game_time: int, *args, **kwargs):
        for terminal in self.terminals:
            terminal.state_machine.think(game_time)


class TerminalView:
    def __init__(self, terminal_controller: TerminalController, img_path: str):
        self.terminal_controller: TerminalController = terminal_controller
        self.image: Surface = image.load(img_path)

    def render(self, surface: Surface):
        for terminal in self.terminal_controller.terminals:
            if terminal.state_machine.active_state == "active":
                surface.blit(self.image, terminal.location)
            elif terminal.state_machine.active_state == "inactive":
                # Optionally render inactive terminals differently
                pass
            elif terminal.state_machine.active_state == "broken":
                # Optionally render broken terminals differently
                pass
            elif terminal.state_machine.active_state == "hacking":
                # Optionally render terminals being hacked differently
                pass
