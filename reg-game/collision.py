import enemy
from config import PLAYER_SIZE, TERMINAL_SIZE
from enemy import MaisyController, MaisyModel
from framework import Game, GameState
from interstitial import InterstitialState
from pygame import Rect
from regplayer import PlayerController, PlayerModel
from terminals import Terminal


class HackerCollisionController:
    def __init__(
        self,
        game: Game,
        maisy_controller: MaisyController,
        player_controller: PlayerController,
        mini_game_state: GameState | None,
        terminals: list[Terminal],
    ) -> None:
        self.game: Game = game
        self.maisy_controller: MaisyController = maisy_controller
        self.player_controller: PlayerController = player_controller
        self.mini_game_state: GameState | None = mini_game_state
        self.terminals: list = terminals

    def update(self, game_time: int, *args, **kwargs) -> None:
        for maisy_model in self.maisy_controller.hacker_models:
            if self.mini_game_state is not None:
                if True in self.hacker_collide_terminal(maisy_model):
                    get_ready_state: InterstitialState = InterstitialState(
                        self.game, "Stop the hacker!", 2000, self.mini_game_state
                    )
                    self.game.change_state(get_ready_state)
                    return

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

    def hacker_collide_terminal(self, maisy_model):
        enemy_width, enemy_height = enemy.PLAYER_SIZE
        maisy_rect: Rect = Rect(maisy_model.x, maisy_model.y, enemy_width, enemy_height)
        collisiions = []
        for terminal in self.terminals:
            collisiion = False
            terminal_x, terminal_y = terminal.location
            terminal_width, terminal_height = TERMINAL_SIZE
            terminal_rect: Rect = Rect(
                terminal_x, terminal_y, terminal_width, terminal_height
            )

            collisiion: bool = maisy_rect.colliderect(terminal_rect)
            collisiions.append(collisiion)

        return collisiions
