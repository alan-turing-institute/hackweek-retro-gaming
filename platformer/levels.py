from platplayer import Player
from pygame.sprite import Group
from constants import BLUE
from pygame.surface import Surface
import pygame
import constants
import platforms
from platforms import Platform, MovingPlatform


class Level:
    def __init__(self, player: Player):
        self.background: Surface | None = None

        self.world_shift: int = 0
        self.level_limit: int = -1000

        self.platform_list: Group = Group()
        self.enemy_list: Group = Group()
        self.player: Player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen: Surface) -> None:
        screen.fill(BLUE)
        if self.background is not None:
            screen.blit(self.background, (self.world_shift // 3, 0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x: int) -> None:
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class FirstLevel(Level):
    def __init__(self, player: Player):
        super().__init__(player)

        self.background: Surface = pygame.image.load("img/background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit: int = -2500

        level: list[list] = [
            [platforms.GRASS_LEFT, 500, 500],
            [platforms.GRASS_MIDDLE, 570, 500],
            [platforms.GRASS_RIGHT, 640, 500],
            [platforms.GRASS_LEFT, 800, 400],
            [platforms.GRASS_MIDDLE, 870, 400],
            [platforms.GRASS_RIGHT, 940, 400],
            [platforms.GRASS_LEFT, 1000, 500],
            [platforms.GRASS_MIDDLE, 1070, 500],
            [platforms.GRASS_RIGHT, 1140, 500],
            [platforms.STONE_PLATFORM_LEFT, 1120, 280],
            [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
            [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
        ]

        for platform in level:
            block: Platform = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]

            block.player = self.player

            self.platform_list.add(block)

        block = MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class SecondLevel(Level):
    def __init__(self, player: Player):
        super().__init__(player)

        self.background: Surface = pygame.image.load("img/background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        level: list[list] = [
            [platforms.STONE_PLATFORM_LEFT, 500, 550],
            [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
            [platforms.STONE_PLATFORM_RIGHT, 640, 550],
            [platforms.GRASS_LEFT, 800, 400],
            [platforms.GRASS_MIDDLE, 870, 400],
            [platforms.GRASS_RIGHT, 940, 400],
            [platforms.GRASS_LEFT, 1000, 500],
            [platforms.GRASS_MIDDLE, 1070, 500],
            [platforms.GRASS_RIGHT, 1140, 500],
            [platforms.STONE_PLATFORM_LEFT, 1120, 280],
            [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
            [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
        ]

        for platform in level:
            block: Platform = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player

            self.platform_list.add(block)

        block = MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
