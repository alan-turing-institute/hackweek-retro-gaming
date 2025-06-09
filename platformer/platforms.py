from typing import Any

import pygame
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface
from spritesheet import SpriteSheet

GRASS_LEFT: tuple[int, int, int, int] = (576, 720, 70, 70)
GRASS_RIGHT: tuple[int, int, int, int] = (576, 576, 70, 70)
GRASS_MIDDLE: tuple[int, int, int, int] = (504, 576, 70, 70)
STONE_PLATFORM_LEFT: tuple[int, int, int, int] = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE: tuple[int, int, int, int] = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT: tuple[int, int, int, int] = (792, 648, 70, 40)


class Platform(Sprite):
    def __init__(self, sprite_sheet_data: tuple[int, int, int, int]) -> None:
        super().__init__()

        sprite_sheet: SpriteSheet = SpriteSheet("img/tiles_spritesheet.png")

        self.image: Surface = sprite_sheet.get_image(
            sprite_sheet_data[0],
            sprite_sheet_data[1],
            sprite_sheet_data[2],
            sprite_sheet_data[3],
        )

        self.rect: Rect = self.image.get_rect()
        self.player: Any = None


class MovingPlatform(Platform):
    def __init__(self, sprite_sheet_data) -> None:
        super().__init__(sprite_sheet_data)

        self.change_x: int = 0
        self.change_y: int = 0

        self.boundary_top: int = 0
        self.boundary_bottom: int = 0
        self.boundary_left: int = 0
        self.boundary_right: int = 0

        self.level: Any = None

    def update(self) -> None:
        self.rect.x += self.change_x

        if self.player is not None:
            hit: bool = pygame.sprite.collide_rect(self, self.player)
            if hit:
                if self.change_x < 0:
                    self.player.rect.right = self.rect.left
                else:
                    self.player.rect.left = self.rect.right

            self.rect.y += self.change_y

            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                if self.change_y < 0:
                    self.player.rect.bottom = self.rect.top
                else:
                    self.player.rect.top = self.rect.bottom

            if (
                self.rect.bottom > self.boundary_bottom
                or self.rect.top < self.boundary_top
            ):
                self.change_y *= -1

        if self.level is not None:
            current_position = self.rect.x - self.level.world_shift

            if (
                current_position < self.boundary_left
                or current_position > self.boundary_right
            ):
                self.change_x *= -1
