from framework import Game
from enemy import MaisyController
from regplayer import PlayerController
from reg_game import GameState


class CollisionController:

    def __init__(
        self,
        game: Game,
        maisy_controller: MaisyController,
        player_controller: PlayerController,
        play_state: GameState,
    ) -> None:
        self.game: Game = game
        self.maisy_controller: MaisyController = maisy_controller
        self.player_controller: PlayerController = player_controller
        self.play_state: GameState = play_state
