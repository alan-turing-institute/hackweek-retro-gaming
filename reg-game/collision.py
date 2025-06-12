import enemy
from config import PLAYER_SIZE, SANDBOX_IMAGE_HEIGHT, SANDBOX_IMAGE_WIDTH, TERMINAL_SIZE
from enemy import MaisyController, MaisyModel
from framework import Game
from pygame import Rect
from regplayer import PlayerController, PlayerModel
from sandbox import SandboxModel
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
        for hacker in self.maisy_controller.hacker_models:
            # Check if hacker collides with a sandbox
            for sandbox in self.player_controller.sandbox_controller.sandbox_models:
                if self.collides_with_sandbox(
                    position_x=hacker.x,
                    position_y=hacker.y,
                    width=enemy.PLAYER_SIZE[0],
                    height=enemy.PLAYER_SIZE[1],
                    sandbox_model=sandbox,
                ):
                    if sandbox.hacker_at_sandbox is None:
                        sandbox.hacker_at_sandbox = hacker
                        hacker.sandbox_controller = (
                            self.player_controller.sandbox_controller
                        )
                        hacker.active_sandbox = sandbox
                    else:
                        sandbox.hacker_at_sandbox = None
                        hacker.active_sandbox = None

                    break

            for terminal in self.terminal_controller.terminals:
                # Check if the hacker collides with the terminal
                if self.collides_with_terminal(
                    position_x=hacker.x,
                    position_y=hacker.y,
                    width=enemy.PLAYER_SIZE[0],
                    height=enemy.PLAYER_SIZE[1],
                    terminal_model=terminal,
                ):
                    terminal.hacker_at_terminal = hacker
                    hacker.active_terminal = terminal
                elif hacker.active_terminal == terminal:
                    terminal.hacker_at_terminal = None
                    hacker.active_terminal = None

                # Check if the player collides with the terminal
                if self.collides_with_terminal(
                    position_x=self.player_controller.player_model.x,
                    position_y=self.player_controller.player_model.y,
                    width=PLAYER_SIZE[0],
                    height=PLAYER_SIZE[1],
                    terminal_model=terminal,
                ):
                    terminal.player_at_terminal = self.player_controller.player_model
                else:
                    terminal.player_at_terminal = None

                break

    def player_collide(self, maisy_model: MaisyModel) -> bool:
        player_model: PlayerModel = self.player_controller.player_model
        player_width, player_height = PLAYER_SIZE
        player_rect: Rect = Rect(
            player_model.x, player_model.y, player_width, player_height
        )

        enemy_width, enemy_height = enemy.PLAYER_SIZE
        maisy_rect: Rect = Rect(maisy_model.x, maisy_model.y, enemy_width, enemy_height)

        collision: bool = player_rect.colliderect(maisy_rect)

        return collision

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

    def collides_with_sandbox(
        self,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        sandbox_model: SandboxModel,
    ) -> bool:
        entity_rect: Rect = Rect(position_x, position_y, width, height)

        sandbox_rect: Rect = Rect(
            sandbox_model.x, sandbox_model.y, SANDBOX_IMAGE_WIDTH, SANDBOX_IMAGE_HEIGHT
        )

        collision: bool = entity_rect.colliderect(sandbox_rect)

        return collision
