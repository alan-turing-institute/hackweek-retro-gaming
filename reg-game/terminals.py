from random import randint

from config import SCREEN_HEIGHT, SCREEN_WIDTH
from framework import State, StateMachine
from pygame import Surface, image
from framework import StateMachine, State
from regplayer import PlayerModel
from enemy import MaisyModel


class ActiveState(State):

    def __init__(self, terminal: "TerminalModel"):
        super().__init__("active")
        self.terminal_model = terminal


class HackingState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("hacking")
        self.terminal_model = terminal


class FixingState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("fixing")
        self.terminal_model = terminal


class BrokenState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("broken")
        self.terminal_model = terminal


class UnHackableState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("unhackable")
        self.terminal_model = terminal


class TerminalModel:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location: tuple[int, int] = location
        self.player_at_terminal: PlayerModel | None = None
        self.hacker_at_terminal: MaisyModel | None = None

        self.state_machine = StateMachine()
        self.state_machine.add_state(ActiveState(self))
        self.state_machine.add_state(HackingState(self))
        self.state_machine.add_state(FixingState(self))
        self.state_machine.add_state(BrokenState(self))

        self.state_machine.set_state("active")

    def set_status(self, new_state: str):
        self.state_machine.set_state(new_state)

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

            if terminal.state_machine.active_state is not None:
                terminal_state: str = terminal.state_machine.active_state.name

                if terminal_state == "active":
                    surface.blit(self.image, terminal.location)
                elif terminal_state == "hacking":
                    pass
                elif terminal_state == "fixing":
                    pass
                elif terminal_state == "broken":
                    pass
                elif terminal_state == "unhackable":
                    pass
