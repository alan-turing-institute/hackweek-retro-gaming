import pygame
from bitmapfont import BitmapFont
from bullet import BulletController
from pygame.key import ScancodeWrapper
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN
from pygame.surface import Surface
from spritesheet import SpriteSheet
from config import (
    PLAYER_SPRITE_WIDTH,
    PLAYER_SPRITE_HEIGHT,
    NUMBER_OF_SPRITES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    PLAYER_SIZE,
)


PLAYER_SPRITESHEET_X: int = 0
PLAYER_SPRITESHEET_Y: int = 0


class PlayerModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        self.lives: int = 3
        self.score: int = 0
        self.speed: int = 100

        self.direction: str = "RIGHT"


class PlayerController:
    def __init__(self, x, y) -> None:
        self.model: PlayerModel = PlayerModel(x, y)
        self.is_paused: bool = False
        self.bullets: BulletController = BulletController(speed=-200)
        self.shoot_sound = pygame.mixer.Sound("sound/playershoot.wav")

    def pause(self, is_paused: bool):
        self.is_paused = is_paused

    def update(self, game_time: int) -> None:
        self.bullets.update(game_time)
        if self.is_paused:
            return

        keys: ScancodeWrapper = pygame.key.get_pressed()

        distance: float = (game_time / 1000.0) * self.model.speed
        if keys[K_RIGHT] and self.model.x < (SCREEN_WIDTH - PLAYER_SIZE[0]):
            self.model.x += distance
            self.model.direction = "RIGHT"
        elif keys[K_LEFT] and self.model.x > 0:
            self.model.x -= distance
            self.model.direction = "LEFT"
        elif keys[K_UP] and self.model.y > 0:
            self.model.y -= distance
            self.model.direction = "UP"
        elif keys[K_DOWN] and self.model.y < (SCREEN_HEIGHT - PLAYER_SIZE[1]):
            self.model.y += distance
            self.model.direction = "DOWN"

        if keys[K_SPACE] and self.bullets.can_fire():
            x = self.model.x + 9
            y = self.model.y - 16
            self.bullets.add_bullet(x, y)
            self.shoot_sound.play()

    def hit(self, x, y, width, height):
        return (
            x >= self.model.x
            and y >= self.model.y
            and x + width <= self.model.x + 32
            and y + height <= self.model.y + 32
        )


class PlayerView:
    def __init__(self, player: PlayerController, sprite_sheet_path: str) -> None:
        self.player_controller: PlayerController = player

        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path)
        self.moving_frames_right: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=2,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_left: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=3,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_up: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=0,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_down: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=1,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.image: Surface = self.moving_frames_right[0]

    def render(self, surface: Surface):
        list_index: int = 0
        if self.player_controller.model.direction == "RIGHT":
            list_index = int(self.player_controller.model.x) % len(
                self.moving_frames_right
            )
            self.image = self.moving_frames_right[list_index]
        elif self.player_controller.model.direction == "LEFT":
            list_index = int(self.player_controller.model.x) % len(
                self.moving_frames_left
            )
            self.image = self.moving_frames_left[list_index]
        elif self.player_controller.model.direction == "UP":
            list_index = int(self.player_controller.model.y) % len(
                self.moving_frames_up
            )
            self.image = self.moving_frames_up[list_index]
        elif self.player_controller.model.direction == "DOWN":
            list_index = int(self.player_controller.model.y) % len(
                self.moving_frames_down
            )
            self.image = self.moving_frames_down[list_index]

        surface.blit(
            self.image,
            (
                self.player_controller.model.x,
                self.player_controller.model.y,
                PLAYER_SPRITE_WIDTH,
                PLAYER_SPRITE_HEIGHT,
            ),
        )


class PlayerLivesView:
    def __init__(self, player: PlayerController, img_path: str) -> None:
        self.player: PlayerController = player
        self.image: Surface = pygame.image.load(img_path)
        self.font: BitmapFont = BitmapFont("img/fasttracker2-style_12x12.png", 12, 12)

    def render(self, surface: Surface):
        x: int = 8
        for _ in range(0, self.player.model.lives):
            surface.blit(self.image, (x, 8, 32, 32))
            x += 40

        self.font.draw(surface, "1UP SCORE: " + str(self.player.model.score), 160, 12)
