import pygame
from bullet import BulletController
from enemy import SwarmController
from framework import Game, GameState
from interstitial import InterstitialState
from pygame.mixer import Sound
from pygame.surface import Surface
from regplayer import PlayerController


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

    def add(self, explosion: tuple, next_state: GameState | None = None):
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
            self.explosions.remove(explosion)

        if next_state is not None:
            self.game.change_state(next_state)


class ExplosionView:
    def __init__(
        self,
        explosions: list[ExplosionModel],
        explosion_img: str,
        width: int,
        height: int,
    ) -> None:
        self.image: Surface = pygame.image.load(explosion_img)
        self.image.set_colorkey((255, 0, 255))

        self.explosions: list[ExplosionModel] = explosions
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

    def update(self, game_time: int, *args, **kwargs):
        for explosion in self.list.explosions:
            explosion.speed -= game_time
            if explosion.speed < 0:
                explosion.speed += explosion.initial_speed
                explosion.frame += 1

        self.list.clean_up()


class CollisionController:
    def __init__(
        self,
        game: Game,
        swarm: SwarmController,
        player: PlayerController,
        explosion_controller,
        play_state,
    ) -> None:
        self.swarm: SwarmController = swarm
        self.player: PlayerController = player
        self.game: Game = game
        self.bullet_controller: BulletController = player.bullets
        self.enemy_bullets: BulletController = swarm.bullets
        self.explosion_controller: ExplosionController = explosion_controller
        self.play_game_state: GameState = play_state
        self.alien_dead_sound: Sound = pygame.mixer.Sound("sound/aliendie.wav")
        self.player_die: Sound = pygame.mixer.Sound("sound/playerdie.wav")

    def update(self, game_time, *args, **kwargs) -> None:
        aliens: list = []
        bullets: list = []

        for bullet in self.bullet_controller.bullets:
            if bullets.count(bullet) > 0:
                continue

            for invader in self.swarm.invaders:
                if invader.hit(bullet.x + 3, bullet.y + 3, 8, 12):
                    aliens.append(invader)
                    bullets.append(bullet)
                    break

        for bullet in bullets:
            self.bullet_controller.remove_bullet(bullet)

        for invader in aliens:
            self.swarm.invaders.remove(invader)
            self.player.model.score += 10 * (invader.alien_type + 1)
            self.explosion_controller.list.add((invader.x, invader.y, 6, 50))
            self.alien_dead_sound.play()

        player_hit: bool = False
        for bullet in self.enemy_bullets.bullets:
            if self.player.hit(bullet.x + 3, bullet.y + 3, 8, 12):
                self.player.model.lives -= 1
                player_hit = True
                break

        if player_hit:
            self.enemy_bullets.clear()
            self.player.bullets.clear()

            if self.player.model.lives > 0:
                self.player.pause(True)

                get_ready_state: InterstitialState = InterstitialState(
                    self.game, "Get ready!", 2000, self.play_game_state
                )
                self.explosion_controller.list.add(
                    (self.player.model.x, self.player.model.y, 6, 50), get_ready_state
                )

            self.player_die.play()
