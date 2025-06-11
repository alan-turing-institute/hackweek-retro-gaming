from random import randint
import pygame

from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UNHACKABLE_COUNTDOWN,
    TERMINAL_IMAGE_SERVER,
    TERMINAL_IMAGE_COMPUTER_ON,
    TERMINAL_IMAGE_COMPUTER_OFF,
    TERMINAL_SIZE,
    HACKING_COUNTDOWN,
)
from framework import State, StateMachine
from pygame import Surface, image
from regplayer import PlayerModel
from interstitial import InterstitialState
from framework import Game, GameState
from regplayer import PlayerController


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
        self.countdown: int = HACKING_COUNTDOWN

    def do_actions(self, game_time):
        self.countdown -= game_time

    def entry_actions(self) -> None:
        self.countdown = HACKING_COUNTDOWN

    def check_conditions(self) -> str | None:
        if self.countdown <= 0:
            return "broken"

        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is not None
        ):
            return "fixing"

        return None


class FixingState(State):
    def __init__(
        self, terminal: "TerminalModel", get_ready_state: InterstitialState, game: Game
    ):
        super().__init__("fixing")
        self.terminal_model: TerminalModel = terminal
        self.get_ready_state: InterstitialState = get_ready_state
        self.game: Game = game

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

    def entry_actions(self) -> None:
        self.game.change_state(self.get_ready_state)


class BrokenState(State):
    def __init__(self, terminal: "TerminalModel", player_model: PlayerModel):
        super().__init__("broken")
        self.terminal_model: TerminalModel = terminal
        self.player_model: PlayerModel = player_model

    def entry_actions(self) -> None:
        self.player_model.lives -= 1


class UnHackableState(State):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("unhackable")
        self.terminal_model = terminal
        self.countdown: int = UNHACKABLE_COUNTDOWN

    def do_actions(self, game_time):
        self.countdown -= game_time

    def entry_actions(self) -> None:
        self.countdown = UNHACKABLE_COUNTDOWN

    def check_conditions(self) -> str | None:
        if self.countdown <= 0:
            return "active"

        return None


class TerminalModel:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location: tuple[int, int] = location
        self.player_at_terminal: PlayerModel | None = None
        self.hacker_at_terminal = None

        self.hacking_failed: bool = False
        self.fixing_failed: bool = True

        self.state_machine = StateMachine()

    def set_status(self, new_state: str):
        self.state_machine.set_state(new_state)

    def __repr__(self):
        return f"Terminal(name={self.name}, location={self.location})"


class TerminalController:
    def __init__(
        self,
        player_controller: PlayerController,
        game: Game,
        mini_game_state: GameState | None,
    ) -> None:

        offset: int = 80
        self.terminals: list[TerminalModel] = [
            TerminalModel("top-left", (offset, offset)),
            TerminalModel("top-right", (SCREEN_WIDTH - offset, offset)),
            TerminalModel("bottom-left", (offset, SCREEN_HEIGHT - offset)),
            TerminalModel(
                "bottom-right", (SCREEN_WIDTH - offset, SCREEN_HEIGHT - offset)
            ),
        ]

        get_ready_state: InterstitialState = InterstitialState(
            game, "Stop the hacker!", 2000, mini_game_state
        )

        for terminal in self.terminals:
            terminal.state_machine.add_state(ActiveState(terminal))
            terminal.state_machine.add_state(HackingState(terminal))
            terminal.state_machine.add_state(
                FixingState(terminal, get_ready_state, game)
            )
            terminal.state_machine.add_state(
                BrokenState(terminal, player_controller.player_model)
            )
            terminal.state_machine.add_state(UnHackableState(terminal))

            terminal.state_machine.set_state("active")

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
        self.current_terminal_image: Surface = image.load(img_path)

    def render(self, surface: Surface):
        new_terminal_image: Surface = self.current_terminal_image

        for terminal in self.terminal_controller.terminals:
            if terminal.state_machine.active_state is not None:
                terminal_state: str = terminal.state_machine.active_state.name

                if terminal_state == "active":
                    new_terminal_image = image.load(TERMINAL_IMAGE_SERVER)
                elif terminal_state == "hacking":
                    # TODO fix later
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_ON)
                elif terminal_state == "fixing":
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_ON)
                elif terminal_state == "broken":
                    new_terminal_image = self.current_terminal_image
                elif terminal_state == "unhackable":
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_OFF)

            new_terminal_image = pygame.transform.scale(
                new_terminal_image, size=TERMINAL_SIZE
            )
            surface.blit(new_terminal_image, terminal.location)
