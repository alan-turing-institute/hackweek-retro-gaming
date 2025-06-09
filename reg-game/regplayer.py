import pygame
from bitmapfont import BitmapFont
from bullet import BulletController
from pygame.key import ScancodeWrapper
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE
from pygame.surface import Surface
from spritesheet import SpriteSheet

PLAYER_SIZE: tuple[int, int] = (96, 96)

PLAYER_SPRITESHEET_X: int = 0
PLAYER_SPRITESHEET_Y: int = 0
PLAYER_SPRITE_WIDTH: int = 48
PLAYER_SPRITE_HEIGHT: int = 48

NUMBER_OF_SPRITES: int = 8


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

        if keys[K_RIGHT] and self.model.x < (800 - 32):
            self.model.x += (game_time / 1000.0) * self.model.speed
            self.model.direction = "RIGHT"
        elif keys[K_LEFT] and self.model.x > 0:
            self.model.x -= (game_time / 1000.0) * self.model.speed
            self.model.direction = "LEFT"

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

        self.walking_frames_left: list[Surface] = self.get_walking_frames_left()
        self.walking_frames_right: list[Surface] = self.get_walking_frames_right()

        self.image: Surface = self.walking_frames_right[0]

    def get_walking_frames_left(self) -> list[Surface]:
        row_offset: int = 2

        sprite_surfaces: list[Surface] = [
            self.sprite_sheet.get_image(
                x=column_offset * PLAYER_SPRITE_WIDTH,
                y=PLAYER_SPRITE_HEIGHT * row_offset,
                width=PLAYER_SPRITE_WIDTH,
                height=PLAYER_SPRITE_HEIGHT,
            )
            for column_offset in range(0, NUMBER_OF_SPRITES)
        ]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def get_walking_frames_right(self) -> list[Surface]:
        row_offset: int = 3

        sprite_surfaces: list[Surface] = [
            self.sprite_sheet.get_image(
                x=PLAYER_SPRITESHEET_X,
                y=PLAYER_SPRITE_HEIGHT * row_offset,
                width=PLAYER_SPRITE_WIDTH,
                height=PLAYER_SPRITE_HEIGHT,
            )
        ]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def render(self, surface: Surface):
        list_index: int = 0
        if self.player_controller.model.direction == "RIGHT":
            list_index = int(self.player_controller.model.x) % len(
                self.walking_frames_right
            )
            self.image = self.walking_frames_right[list_index]
        elif self.player_controller.model.direction == "LEFT":
            list_index = int(self.player_controller.model.x) % len(
                self.walking_frames_left
            )
            self.image = self.walking_frames_left[list_index]

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
