from framework import Game
from enemy import MaisyController
from regplayer import PlayerController, PlayerModel
from reg_game import GameState
from enemy import MaisyModel
from pygame import Rect
from config import PLAYER_SIZE
import enemy


class CollisionController:

    def __init__(
        self,
        game: Game,
        maisy_controller: MaisyController,
        player_controller: PlayerController,
        mini_game_state: GameState | None,
    ) -> None:
        self.game: Game = game
        self.maisy_controller: MaisyController = maisy_controller
        self.player_controller: PlayerController = player_controller
        self.mini_game_state: GameState | None = mini_game_state

    def update(self, game_time: int, *args, **kwargs) -> None:

        for maisy_model in self.maisy_controller.hacker_models:
            if self.mini_game_state is not None:
                if self.player_collide(maisy_model):
                    self.game.change_state(self.mini_game_state)
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
