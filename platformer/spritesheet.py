import pygame
import constants
from pygame.surface import Surface


class SpriteSheet:
    def __init__(self, file_name: str):
        self.sprite_sheet: Surface = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height) -> Surface:

        image: Surface = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.BLACK)

        return image