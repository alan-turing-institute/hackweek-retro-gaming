import pygame
from bitmapfont import BitmapFont
from config import (
    LIVES_MESSAGE_X,
    LIVES_MESSAGE_Y,
    LIVES_SPRITE_HEIGHT,
    LIVES_SPRITE_WIDTH,
    NUMBER_OF_LIVES,
    PLAYER_FACING_DOWN_OFFSET,
    PLAYER_FACING_LEFT_OFFSET,
    PLAYER_FACING_RIGHT_OFFSET,
    PLAYER_FACING_UP_OFFSET,
    PLAYER_NUMBER_OF_SPRITES,
    PLAYER_SIZE,
    PLAYER_SPRITE_HEIGHT,
    PLAYER_SPRITE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from pygame.key import ScancodeWrapper
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP
from pygame.surface import Surface
from sandbox import SandboxController
from sounds import SoundEffectPlayer
from spritesheet import SpriteSheet

PLAYER_SPRITESHEET_X: int = 0
PLAYER_SPRITESHEET_Y: int = 0


class PlayerModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        self.lives: int = NUMBER_OF_LIVES
        self.score: int = 0
        self.speed: int = 200

        self.direction: str = "RIGHT"


class PlayerController:
    def __init__(self, x, y) -> None:
        self.player_model: PlayerModel = PlayerModel(x, y)
        self.is_paused: bool = False
        self.sandbox_controller = SandboxController()
        self.sound_effect_player = SoundEffectPlayer()

    def pause(self, is_paused: bool):
        self.is_paused = is_paused

    def update(self, game_time: int, *args, **kwargs) -> None:
        self.sandbox_controller.update(game_time)
        if self.is_paused:
            return

        keys: ScancodeWrapper = pygame.key.get_pressed()

        distance: float = (game_time / 1000.0) * self.player_model.speed
        if keys[K_RIGHT] and self.player_model.x < (SCREEN_WIDTH - PLAYER_SIZE[0]):
            self.player_model.x += distance
            self.player_model.direction = "RIGHT"
        elif keys[K_LEFT] and self.player_model.x > 0:
            self.player_model.x -= distance
            self.player_model.direction = "LEFT"
        elif keys[K_UP] and self.player_model.y > 0:
            self.player_model.y -= distance
            self.player_model.direction = "UP"
        elif keys[K_DOWN] and self.player_model.y < (SCREEN_HEIGHT - PLAYER_SIZE[1]):
            self.player_model.y += distance
            self.player_model.direction = "DOWN"

        if keys[K_SPACE] and self.sandbox_controller.is_sandbox_available():
            x = self.player_model.x + 9
            y = self.player_model.y - 16
            self.sandbox_controller.add_sandbox(x, y)
            self.sound_effect_player.play_sandbox_sound()


class PlayerView:
    def __init__(self, player: PlayerController, sprite_sheet_path: str) -> None:
        self.player_controller: PlayerController = player

        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path)
        self.moving_frames_right: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=PLAYER_FACING_RIGHT_OFFSET,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=PLAYER_NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_left: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=PLAYER_FACING_LEFT_OFFSET,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=PLAYER_NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_up: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=PLAYER_FACING_UP_OFFSET,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=PLAYER_NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.moving_frames_down: list[Surface] = self.sprite_sheet.get_frames_in_row(
            row_offset=PLAYER_FACING_DOWN_OFFSET,
            sprite_width=PLAYER_SPRITE_WIDTH,
            sprite_height=PLAYER_SPRITE_HEIGHT,
            number_of_sprites=PLAYER_NUMBER_OF_SPRITES,
            target_size=PLAYER_SIZE,
        )

        self.image: Surface = self.moving_frames_right[0]

    def render(self, surface: Surface):
        list_index: int = 0
        if self.player_controller.player_model.direction == "RIGHT":
            list_index = int(self.player_controller.player_model.x) % len(
                self.moving_frames_right
            )
            self.image = self.moving_frames_right[list_index]
        elif self.player_controller.player_model.direction == "LEFT":
            list_index = int(self.player_controller.player_model.x) % len(
                self.moving_frames_left
            )
            self.image = self.moving_frames_left[list_index]
        elif self.player_controller.player_model.direction == "UP":
            list_index = int(self.player_controller.player_model.y) % len(
                self.moving_frames_up
            )
            self.image = self.moving_frames_up[list_index]
        elif self.player_controller.player_model.direction == "DOWN":
            list_index = int(self.player_controller.player_model.y) % len(
                self.moving_frames_down
            )
            self.image = self.moving_frames_down[list_index]

        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        surface.blit(
            self.image,
            (
                self.player_controller.player_model.x,
                self.player_controller.player_model.y,
                PLAYER_SPRITE_WIDTH,
                PLAYER_SPRITE_HEIGHT,
            ),
        )


class PlayerLivesView:
    def __init__(self, player: PlayerController, img_path: str) -> None:
        self.player: PlayerController = player

        sprite_sheet: SpriteSheet = SpriteSheet(img_path)
        self.image: Surface = sprite_sheet.get_image(
            x=LIVES_SPRITE_WIDTH * 3,
            y=0,
            width=LIVES_SPRITE_WIDTH,
            height=LIVES_SPRITE_HEIGHT,
        )

        self.font: BitmapFont = BitmapFont("img/fasttracker2-style_12x12.png", 12, 12)

    def render(self, surface: Surface):
        x: int = 8
        for _ in range(0, self.player.player_model.lives):
            surface.blit(self.image, (x, 8, 32, 32))
            x += 40

        self.font.draw(
            surface,
            "REGINA SCORE: " + str(self.player.player_model.score),
            LIVES_MESSAGE_X,
            LIVES_MESSAGE_Y,
        )
