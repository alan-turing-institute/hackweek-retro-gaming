from random import randint

from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TERMINAL_IMAGE_HEIGHT,
    TERMINAL_IMAGE_WIDTH,
    TERMINAL_SPRITE_SHEET,
)

# from enemy import MaisyModel
from framework import State, StateMachine
from pygame import Surface, image
from regplayer import PlayerModel
from spritesheet import SpriteSheet


class ActiveState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("active")
        self.terminal_model = terminal

    def check_conditions(self) -> str | None:
        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is None
        ):
            return "hacking"
        return None


class HackingState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("hacking")
        self.terminal_model = terminal

    def check_conditions(self) -> str | None:
        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is not None
        ):
            return "fixing"

        return None


class FixingState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("fixing")
        self.terminal_model = terminal

    def check_conditions(self) -> str | None:
        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is not None
            and self.terminal_model.hacking_failed
        ):
            return "unhackable"

        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is not None
            and self.terminal_model.fixing_failed
        ):
            return "broken"

        return None


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
        self.hacker_at_terminal = None

        self.hacking_failed: bool = False
        self.fixing_failed: bool = True

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

        offset: int = 50
        self.terminals: list[TerminalModel] = [
            TerminalModel("top-left", (offset, offset)),
            TerminalModel("top-right", (SCREEN_WIDTH - offset, offset)),
            TerminalModel("bottom-left", (offset, SCREEN_HEIGHT - offset)),
            TerminalModel(
                "bottom-right", (SCREEN_WIDTH - offset, SCREEN_HEIGHT - offset)
            ),
        ]

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
        sprite_sheet: SpriteSheet = SpriteSheet(TERMINAL_SPRITE_SHEET)
        new_terminal_image: Surface = self.image

        for terminal in self.terminal_controller.terminals:
            if terminal.state_machine.active_state is not None:
                terminal_state: str = terminal.state_machine.active_state.name

                if terminal_state == "active":
                    new_terminal_image = self.image
                elif terminal_state == "hacking":
                    # TODO fix later
                    new_terminal_image = sprite_sheet.get_image(
                        TERMINAL_IMAGE_WIDTH * 2,
                        0,
                        TERMINAL_IMAGE_WIDTH,
                        TERMINAL_IMAGE_HEIGHT,
                    )
                elif terminal_state == "fixing":
                    new_terminal_image = sprite_sheet.get_image(
                        TERMINAL_IMAGE_WIDTH * 2,
                        0,
                        TERMINAL_IMAGE_WIDTH,
                        TERMINAL_IMAGE_HEIGHT,
                    )
                elif terminal_state == "broken":
                    new_terminal_image = sprite_sheet.get_image(
                        TERMINAL_IMAGE_WIDTH * 2,
                        TERMINAL_IMAGE_HEIGHT * 2,
                        TERMINAL_IMAGE_WIDTH,
                        TERMINAL_IMAGE_HEIGHT,
                    )
                elif terminal_state == "unhackable":
                    new_terminal_image = sprite_sheet.get_image(
                        0,
                        TERMINAL_IMAGE_HEIGHT * 2,
                        TERMINAL_IMAGE_WIDTH,
                        TERMINAL_IMAGE_HEIGHT,
                    )

            surface.blit(new_terminal_image, terminal.location)
