from bullet import BulletView
from colission import CollisionController, ExplosionController, ExplosionView
from framework import Game, GameState
from interstitial import InterstitialState
from invplayer import PlayerController, PlayerLivesView, PlayerView
from swarm import InvaderView, SwarmController

# from invaders import invaders_game


class PlayGameState(GameState):
    def __init__(self, game: Game, game_over_state: GameState) -> None:
        super().__init__(game)
        self.controllers: list | None = None
        self.renderers: list | None = None
        self.player_controller = None
        self.swarm_controller = None
        self.swarm_speed: int = 500
        self.game_over_state = game_over_state

        self.initialise()

    def on_enter(self, previous_state: GameState | None):
        if self.player_controller is not None:
            self.player_controller.pause(False)

    def initialise(self):
        self.swarm_controller = SwarmController(800, 48, self.swarm_speed)
        swarm_renderer = InvaderView(self.swarm_controller, "img/invaders.png")

        self.player_controller = PlayerController(0, 540)

        player_renderer = PlayerView(self.player_controller, "img/ship.png")
        lives_renderer = PlayerLivesView(self.player_controller, "img/ship.png")
        bullet_renderer = BulletView(self.player_controller.bullets, "img/bullet.png")
        alien_bullet_renderer = BulletView(
            self.swarm_controller.bullets, "img/alienbullet.png"
        )
        explosion_controller = ExplosionController(self.game)
        collision_controller = CollisionController(
            self.game,
            self.swarm_controller,
            self.player_controller,
            explosion_controller,
            self,
        )
        explosion_view = ExplosionView(
            explosion_controller.list.explosions, "img/explosion.png", 32, 32
        )

        self.renderers = [
            alien_bullet_renderer,
            swarm_renderer,
            bullet_renderer,
            player_renderer,
            lives_renderer,
            explosion_view,
        ]

        self.controllers = [
            self.swarm_controller,
            self.player_controller,
            collision_controller,
            explosion_controller,
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

        if (
            self.swarm_controller is not None
            and len(self.swarm_controller.invaders) == 0
        ):
            self.swarm_speed -= 50
            if self.swarm_speed < 100:
                self.swarm_speed = 100

            self.swarm_controller.reset(48, self.swarm_speed)
            level_up_message = InterstitialState(
                self.game, "Congratulations! Level up", 2000, self
            )
            self.game.change_state(level_up_message)

    def draw(self, surface):
        for view in self.renderers:
            view.render(surface)
