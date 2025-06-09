import random
import sys

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.time import Clock

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)

FRAME_RATE: int = 60
SCREEN_SIZE: tuple[int, int] = (500, 800)


def main() -> None:
    pygame.init()

    clock: Clock = Clock()
    clock.tick(FRAME_RATE)
    pygame.display.set_caption("Crazy Driver")

    road_image: Surface = pygame.image.load("img/Road.png")
    player_image: Surface = pygame.image.load("img/Player.png")
    enemy_image: Surface = pygame.image.load("img/Enemy.png")

    screen: Surface = pygame.display.set_mode(road_image.get_size())

    sprite_center_x: int = road_image.get_width() // 2
    sprite_center_y: int = road_image.get_height() - player_image.get_height() // 2
    player: Sprite = Sprite()
    player.image = player_image
    player.surf = Surface(player_image.get_size())
    player.rect = player.surf.get_rect(center=(sprite_center_x, sprite_center_y))

    sprite_center_min: int = enemy_image.get_width() // 2
    sprite_center_max: int = road_image.get_width() - enemy_image.get_width() // 2
    sprite_center_x = random.randrange(sprite_center_min, sprite_center_max)
    sprite_center_y = 0
    enemy: Sprite = Sprite()
    enemy.image = enemy_image
    enemy.surf = Surface(enemy_image.get_size())
    enemy.rect = enemy.surf.get_rect(center=(sprite_center_x, sprite_center_y))

    while True:
        screen.blit(road_image, (0, 0))

        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
