from typing import Any

import constants
import pygame
from platforms import MovingPlatform
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface
from spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.change_x: float = 0
        self.change_y: float = 0

        self.walking_frames_left: list[Surface] = []
        self.walking_frames_right: list[Surface] = []

        self.direction: str = "R"

        self.level: Any = None

        sprite_sheet: SpriteSheet = SpriteSheet("img/p1_walk.png")
        image: Surface = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_right.append(image)

        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_left.append(image)

        self.image: Surface = self.walking_frames_right[0]
        self.rect: Rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        self.calculate_gravity()

        self.rect.x += self.change_x  # type: ignore

        if self.level is not None:
            position: int = self.rect.x + self.level.world_shift
            if self.direction == "R":
                frame_index: int = (position // 30) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[frame_index]
            else:
                frame_index = (position // 30) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[frame_index]

            block_hist_list: list = pygame.sprite.spritecollide(
                self, self.level.platform_list, False
            )
            for block in block_hist_list:
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

            self.rect.y += self.change_y  # type: ignore
            block_hist_list = pygame.sprite.spritecollide(
                self, self.level.platform_list, False
            )

            for block in block_hist_list:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                self.change_y = 0

                if isinstance(block, MovingPlatform):
                    self.rect.x += block.change_x

    def calculate_gravity(self) -> None:
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        if (
            self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height
            and self.change_y >= 0
        ):
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self) -> None:
        if self.level is not None:
            self.rect.y += 2
            platform_hit_list: list[Sprite] = pygame.sprite.spritecollide(
                self, self.level.platform_list, False
            )
            self.rect.y -= 2

            if (
                len(platform_hit_list) > 0
                or self.rect.bottom >= constants.SCREEN_HEIGHT
            ):
                self.change_y -= 10

    def go_left(self) -> None:
        self.change_x = -6
        self.direction = "L"

    def go_right(self) -> None:
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        self.change_x = 0
