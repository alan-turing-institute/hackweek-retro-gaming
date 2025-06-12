from background import BackgroundView
from collision import HackerCollisionController
from config import (
    LIVES_SPRITE_SHEET_PATH,
    MAIN_GAME_MAX_TIME,
    NUMBER_OF_LIVES,
    PLAYER_SPRITE_SHEET_PATH,
    SANDBOX_IMAGE_PATH,
    SCREEN_WIDTH,
)
from enemy import MaisyController, MaisyView
from framework import Game, GameState
from interstitial import InterstitialState
from regplayer import PlayerController, PlayerLivesView, PlayerView
from sandbox import SandboxView
from sounds import MusicPlayer
from terminals import TerminalController, TerminalView

PLAYER_X: int = SCREEN_WIDTH // 2
PLAYER_Y: int = 500


class PlayGameState(GameState):
    def __init__(self, game: Game, game_over_state: GameState) -> None:
        super().__init__(game)
        self.controllers: list | None = None
        self.renderers: list | None = None
        self.player_controller: PlayerController | None = None
        self.game_over_state: GameState | None = game_over_state
        self.game_time: int = 0
        self.initialise()

    def on_enter(self, previous_state: GameState | None):
        if self.player_controller is not None:
            self.player_controller.pause(False)

    def initialise(self) -> None:
        self.music_player = MusicPlayer()
        self.music_player.start()
        self.maisy_controller = MaisyController()
        self.player_controller = PlayerController(x=PLAYER_X, y=PLAYER_Y)
        self.terminal_controller = TerminalController(
            self.player_controller,
            self.game,
            play_game_state=self,
            game_over_state=self.game_over_state,
        )
        self.collision_controller = HackerCollisionController(
            self.game,
            self.maisy_controller,
            self.player_controller,
            self.terminal_controller,
        )

        background_renderer = BackgroundView("img/industrial_floor.png")

        player_renderer = PlayerView(self.player_controller, PLAYER_SPRITE_SHEET_PATH)
        maisy_renderer = MaisyView(self.maisy_controller, "img/maisy_model_lr.png")
        lives_renderer = PlayerLivesView(
            self.player_controller, LIVES_SPRITE_SHEET_PATH
        )
        sandbox_renderer = SandboxView(
            self.player_controller.sandbox_controller, SANDBOX_IMAGE_PATH
        )
        terminal_renderer = TerminalView(
            self.terminal_controller, "img/CommTerminal.png"
        )  # terminal image is 32 x 32 pixels

        self.renderers = [
            background_renderer,
            sandbox_renderer,
            player_renderer,
            lives_renderer,
            maisy_renderer,
            terminal_renderer,
        ]

        self.controllers = [
            self.player_controller,
            self.maisy_controller,
            self.collision_controller,
            self.terminal_controller,
        ]

    def update(self, game_time: int, *args, **kwargs):
        self.game_time += game_time
        if (
            self.game_time >= MAIN_GAME_MAX_TIME
            or self.player_controller.player_model.lives == 0
        ):
            self.game_time = 0
            if self.player_controller.player_model.lives == 0:
                # all machines have been compromised
                message = "You have failed us solider!!!\n\nAll our machines have been compromised!\nYou were USELESS out there!\n\nWe will never recover from this."
            elif self.player_controller.player_model.lives == NUMBER_OF_LIVES:
                # all machines have been defended
                message = "Well done soldier!!!\n\nYou have successfully defended all our machines!\n\nWe will never forget your bravery!"
            else:
                # some machines have been compromised
                if self.player_controller.player_model.score >= 0:
                    message = "Well done soldier!\n\nSome machines have been compromised, but you helped save some.\n\nWe live to fight another day."
                else:
                    message = "You have failed us soldier!!!\n\nSome machines have been compromised but at least not all.\n\nYou need to do better next time."

            game_over_state = InterstitialState(
                game=self.game,
                message=message,
                wait_time_ms=10000,
                next_state=self.game_over_state,
            )
            self.game.change_state(game_over_state)

        if self.controllers is not None:
            for controller in self.controllers:
                controller.update(game_time)

        if (
            self.player_controller is not None
            and self.player_controller.player_model.lives == 0
        ):
            self.game.change_state(self.game_over_state)

    def draw(self, surface):
        if self.renderers is not None:
            for view in self.renderers:
                view.render(surface)
