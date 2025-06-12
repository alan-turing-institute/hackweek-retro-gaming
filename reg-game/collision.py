import enemy
from config import PLAYER_SIZE, TERMINAL_SIZE
from enemy import MaisyController, MaisyModel
from framework import Game
from pygame import Rect
from regplayer import PlayerController, PlayerModel
from terminals import TerminalController, TerminalModel


class HackerCollisionController:
    def __init__(
        self,
        game: Game,
        maisy_controller: MaisyController,
        player_controller: PlayerController,
        terminal_controller: TerminalController,
    ) -> None:
        self.game: Game = game
        self.maisy_controller: MaisyController = maisy_controller
        self.player_controller: PlayerController = player_controller
        self.terminal_controller: TerminalController = terminal_controller

    def update(self, game_time: int, *args, **kwargs) -> None:
        for terminal in self.terminal_controller.terminals:
            for hacker in self.maisy_controller.hacker_models:
                if self.collides_with_terminal(
                    hacker.x,
                    hacker.y,
                    enemy.PLAYER_SIZE[0],
                    enemy.PLAYER_SIZE[1],
                    terminal,
                ):
                    print(
                        f"Collision happened: {terminal.state_machine.active_state.name=}"
                    )
                    terminal.hacker_at_terminal = hacker
                    hacker.active_terminal = terminal
                else:
                    terminal.hacker_at_terminal = None
                    hacker.active_terminal = None

                if self.collides_with_terminal(
                    self.player_controller.player_model.x,
                    self.player_controller.player_model.y,
                    PLAYER_SIZE[0],
                    PLAYER_SIZE[1],
                    terminal,
                ):
                    terminal.player_at_terminal = self.player_controller.player_model
                else:
                    terminal.player_at_terminal = None

    def player_collide(self, maisy_model: MaisyModel) -> bool:
        player_model: PlayerModel = self.player_controller.player_model
        player_width, player_height = PLAYER_SIZE
        player_rect: Rect = Rect(
            player_model.x, player_model.y, player_width, player_height
        )

        enemy_width, enemy_height = enemy.PLAYER_SIZE
        maisy_rect: Rect = Rect(maisy_model.x, maisy_model.y, enemy_width, enemy_height)

        result: bool = player_rect.colliderect(maisy_rect)

        return result

    def collides_with_terminal(
        self,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        terminal_model: TerminalModel,
    ) -> bool:
        entity_rect: Rect = Rect(position_x, position_y, width, height)

        terminal_width, terminal_height = TERMINAL_SIZE
        terminal_rect: Rect = Rect(
            terminal_model.location[0],
            terminal_model.location[1],
            terminal_width,
            terminal_height,
        )

        collision: bool = entity_rect.colliderect(terminal_rect)

        return collision
