import pygame
from pygame.surface import Surface

BACKGROUND_COLOR: tuple[int, int, int] = (215, 219, 171)


class SpriteSheet:
    def __init__(self, file_name: str):
        self.sprite_sheet: Surface = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height) -> Surface:

        image: Surface = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # image.set_colorkey(BACKGROUND_COLOR)

        return image
