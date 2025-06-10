from bullet import BulletView
from colission import ExplosionController, ExplosionView
from config import SCREEN_WIDTH
from enemy import MaisyController, MaisyView
from framework import Game, GameState
from regplayer import PlayerController, PlayerLivesView, PlayerView
from terminals import TerminalView, create_random_terminals

PLAYER_X: int = SCREEN_WIDTH // 2
PLAYER_Y: int = 500


class PlayGameState(GameState):
    def __init__(self, game: Game, game_over_state: GameState) -> None:
        super().__init__(game)
        self.controllers: list | None = None
        self.renderers: list | None = None
        self.player_controller = None

        self.game_over_state = game_over_state

        self.initialise()

    def on_enter(self, previous_state: GameState | None):
        if self.player_controller is not None:
            self.player_controller.pause(False)

    def initialise(self):
        # Initialize the terminals
        self.terminals = create_random_terminals(3)
        self.maisy_controller = MaisyController(
            800, 600
        )  # TODO read this from the game

        self.player_controller = PlayerController(x=PLAYER_X, y=PLAYER_Y)

        player_renderer = PlayerView(
            self.player_controller, "img/pixel_character_dark_blue.png"
        )
        maisy_renderer = MaisyView(self.maisy_controller)
        lives_renderer = PlayerLivesView(self.player_controller, "img/ship.png")
        bullet_renderer = BulletView(self.player_controller.bullets, "img/bullet.png")
        explosion_controller = ExplosionController(self.game)
        explosion_view = ExplosionView(
            explosion_controller.list.explosions, "img/explosion.png", 32, 32
        )
        terminal_renderer = TerminalView(
            self.terminals, "img/CommTerminal.png"
        )  # terminal image is 32 x 32 pixels

        self.renderers = [
            bullet_renderer,
            player_renderer,
            lives_renderer,
            explosion_view,
            maisy_renderer,
            terminal_renderer,
        ]

        self.controllers = [
            self.player_controller,
            explosion_controller,
            self.maisy_controller,
        ]

    def update(self, game_time: int):
        if self.controllers is not None:
            for controller in self.controllers:
                controller.update(game_time)

        if (
            self.player_controller is not None
            and self.player_controller.model.lives == 0
        ):
            self.game.change_state(self.game_over_state)

    def draw(self, surface):
        if self.renderers is not None:
            for view in self.renderers:
                view.render(surface)
