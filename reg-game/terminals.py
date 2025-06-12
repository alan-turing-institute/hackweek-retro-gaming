from random import randint
from typing import Any, Optional

import pygame
from config import (
    FIXING_SCORE,
    HACKED_PENALTY,
    HACKING_COUNTDOWN,
    NUMBER_OF_TERMINALS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TERMINAL_IMAGE_COMPUTER_OFF,
    TERMINAL_IMAGE_COMPUTER_ON,
    TERMINAL_SIZE,
    UNHACKABLE_COUNTDOWN,
)
from framework import EntityState, EntityStateMachine, Game, GameState
from interstitial import InterstitialState
from pipe_game import PipeGameState
from pygame import Surface, image
from regplayer import PlayerController, PlayerModel
from sounds import SoundEffectPlayer


class ActiveState(EntityState):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("active")
        self.terminal_model = terminal

    def entry_actions(self):
        pass

    def check_conditions(self) -> str | None:
        print(
            f"Active state {self.terminal_model.hacker_at_terminal=} {self.terminal_model.player_at_terminal=}"
        )
        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is None
        ):
            return "hacking"
        return None


class HackingState(EntityState):
    def __init__(self, terminal: "TerminalModel"):
        super().__init__("hacking")
        self.terminal_model = terminal
        self.countdown: int = HACKING_COUNTDOWN

        self.sound_effect_player: SoundEffectPlayer = SoundEffectPlayer()

    def do_actions(self, game_time):
        self.countdown -= game_time

    def entry_actions(self) -> None:
        self.countdown = HACKING_COUNTDOWN
        self.sound_effect_player.play_hacker_alert()

    def check_conditions(self) -> str | None:
        if self.countdown <= 0:
            return "broken"

        if (
            self.terminal_model.hacker_at_terminal is not None
            and self.terminal_model.player_at_terminal is not None
        ):
            return "fixing"

        return None


class FixingState(EntityState):
    def __init__(
        self,
        terminal: "TerminalModel",
        player: PlayerModel,
        game: Game,
        play_game_state: GameState,
        game_over_state: GameState,
    ):
        super().__init__("fixing")
        self.terminal_model: TerminalModel = terminal
        self.player_model: PlayerModel = player

        mini_game_state: PipeGameState = PipeGameState(
            game=game,
            current_terminal=terminal,
            play_game_state=play_game_state,
            game_over_state=game_over_state,
        )
        self.get_ready_state: InterstitialState = InterstitialState(
            game, "Stop the hacker!", 2000, mini_game_state
        )

        self.game: Game = game

    def check_conditions(self) -> str | None:
        if self.terminal_model.hacking_failed:
            self.player_model.score += FIXING_SCORE
            return "unhackable"

        if self.terminal_model.fixing_failed:
            return "broken"

        return None

    def entry_actions(self) -> None:
        print("Entering Fixing State")
        self.game.change_state(self.get_ready_state)


class BrokenState(EntityState):
    def __init__(
        self,
        terminal: "TerminalModel",
        player_model: PlayerModel,
        game: Game,
        play_game_state: GameState,
    ):
        super().__init__("broken")
        self.terminal_model: TerminalModel = terminal
        self.player_model: PlayerModel = player_model

        self.game: Game = game
        self.play_game_state: GameState = play_game_state

    def entry_actions(self) -> None:
        self.player_model.lives -= 1
        self.terminal_model.fixing_failed = False
        self.player_model.score -= HACKED_PENALTY

        time_out: InterstitialState = InterstitialState(
            self.game,
            "Time run out! The terminal was hacked",
            2000,
            self.play_game_state,
        )
        self.game.change_state(time_out)

        print(f"State changed to Broken. Player lives left: {self.player_model.lives}")

    def check_conditions(self) -> str | None:
        print("Going to unhackable")

        return "unhackable"


class UnHackableState(EntityState):
    def __init__(self, terminal: "TerminalModel", player_model: PlayerModel):
        super().__init__("unhackable")
        self.terminal_model = terminal
        self.countdown: int = UNHACKABLE_COUNTDOWN
        self.player_model: PlayerModel = player_model

    def do_actions(self, game_time):
        self.countdown -= game_time

    def entry_actions(self) -> None:
        self.countdown = UNHACKABLE_COUNTDOWN
        self.terminal_model.hacking_failed = False
        print(f"State changed to UnHackable. Player score: {self.player_model.score}")

    def check_conditions(self) -> str | None:
        if self.countdown <= 0:
            print("Unhackable state countdown finished, going back to active")
            return "active"

        return None


class TerminalModel:
    def __init__(self, name: str, location: tuple[int, int]):
        self.name = name
        self.location: tuple[int, int] = location
        self.player_at_terminal: PlayerModel | None = None
        self.hacker_at_terminal: Optional[Any] = None

        self.hacking_failed: bool = False
        self.fixing_failed: bool = True

        self.state_machine = EntityStateMachine()

    def set_status(self, new_state: str):
        self.state_machine.set_state(new_state)

    def __repr__(self):
        return f"Terminal(name={self.name}, location={self.location})"


class TerminalController:
    def __init__(
        self,
        player_controller: PlayerController,
        game: Game,
        play_game_state: GameState,
        game_over_state: GameState,
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

        self.terminals = self.terminals[:NUMBER_OF_TERMINALS]

        for terminal in self.terminals:
            terminal.state_machine.add_state(ActiveState(terminal))
            terminal.state_machine.add_state(HackingState(terminal))
            terminal.state_machine.add_state(
                FixingState(
                    terminal=terminal,
                    player=player_controller.player_model,
                    game=game,
                    play_game_state=play_game_state,
                    game_over_state=game_over_state,
                )
            )
            terminal.state_machine.add_state(
                BrokenState(
                    terminal=terminal,
                    player_model=player_controller.player_model,
                    game=game,
                    play_game_state=play_game_state,
                )
            )
            terminal.state_machine.add_state(
                UnHackableState(
                    terminal=terminal, player_model=player_controller.player_model
                )
            )

            terminal.state_machine.set_state("active")

    def create_random_terminals(self, num_terminals: int):
        for _ in range(num_terminals):
            x = randint(0, SCREEN_WIDTH - 32)
            y = randint(0, SCREEN_HEIGHT - 32)
            terminal = TerminalModel(name=f"Terminal {_ + 1}", location=(x, y))
            self.terminals.append(terminal)

    def update(self, game_time: int, *args, **kwargs):
        for terminal in self.terminals:
            # TODO: Remove later
            if terminal.state_machine.active_state is not None:
                print(f"{terminal.state_machine.active_state.name=}")

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
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_OFF)
                elif terminal_state == "hacking":
                    # TODO fix later
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_ON)
                elif terminal_state == "fixing":
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_ON)
                elif terminal_state == "broken":
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_OFF)
                elif terminal_state == "unhackable":
                    new_terminal_image = image.load(TERMINAL_IMAGE_COMPUTER_ON)

            new_terminal_image = pygame.transform.scale(
                new_terminal_image, size=TERMINAL_SIZE
            )
            surface.blit(new_terminal_image, terminal.location)
