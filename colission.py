import pygame
from bullet import BulletController
from game import Game, GameState
from pygame.surface import Surface
from pygame.mixer import Sound

from player import PlayerController
from swarm import SwarmController


class ExplosionModel:

    def __init__(self, x, y, max_frames, speed, next_state: GameState | None) -> None:
        self.x = x
        self.y = y
        self.max_frames = max_frames
        self.speed = speed
        self.initial_speed = speed
        self.frame: int = 0
        self.next_state: GameState | None = next_state


class ExplosionModelList:

    def __init__(self, game: Game) -> None:
        self.explosions: list[ExplosionModel] = []
        self.game: Game = game

    def add(self, explosion: tuple, next_state: None):
        x, y, frames, speed = explosion

        explosion_model: ExplosionModel = ExplosionModel(
            x, y, frames, speed, next_state
        )
        self.explosions.append(explosion_model)

    def clean_up(self) -> None:
        kill_list: list[ExplosionModel] = []
        for explosion in self.explosions:
            if explosion.frame == explosion.max_frames:
                kill_list.append(explosion)

        next_state = None
        for explosion in kill_list:
            if next_state is None and explosion.next_state is not None:
                next_state = explosion.next_state

        if next_state is not None:
            self.game.change_state(next_state)


class ExplosionView:

    def __init__(self, explosions, explosion_img, width, height) -> None:
        self.image: Surface = pygame.image.load(explosion_img)
        self.image.set_colorkey((255, 0, 255))

        self.explosions = explosions
        self.width = width
        self.height = height

    def render(self, surface: Surface) -> None:
        for explosion in self.explosions:
            surface.blit(
                self.image,
                (explosion.x, explosion.y, self.width, self.height),
                (explosion.frame * self.width, 0, self.width, self.height),
            )


class ExplosionController:

    def __init__(self, game: Game) -> None:
        self.list: ExplosionModelList = ExplosionModelList(game)

    def update(self, game_time: int):
        for explosion in self.list.explosions:
            explosion.speed -= game_time
            if explosion.speed < 0:
                explosion.speed += explosion.initial_speed
                explosion.frame += 1

        self.list.clean_up()


class CollisionController:

    def __init__(
        self,
        game,
        swarm: SwarmController,
        player: PlayerController,
        explosion_controller,
        play_state,
    ) -> None:
        self.swarm = swarm
        self.player: PlayerController = player
        self.game = game
        self.bullet_controller: BulletController = player.bullets
        self.enemy_bullets: BulletController = swarm.bullets
        self.explosion_controller = explosion_controller
        self.play_game_state = play_state
        self.alien_dead_sound: Sound = pygame.mixer.Sound("sound/aliendie.wav")
        self.player_die: Sound = pygame.mixer.Sound("sound/playerdie.wav")
