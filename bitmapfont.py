import pygame
from pygame.surface import Surface


class BitmapFont:
    def __init__(self, font_file, cell_width: int, cell_height: int) -> None:
        self.image = pygame.image.load(font_file)
        self.cell_width = cell_width
        self.cell_height = cell_height

        width: int = self.image.get_rect().width
        height: int = self.image.get_rect().height
        self.columns = width / self.cell_width
        self.rows = height / self.cell_height

    def draw(self, surface: Surface, message: str, x: int, y: int):
        for character in message:
            index = self.to_index(character)
            offset_x = (index % self.columns) * self.cell_width
            offset_y = (index / self.columns) * self.cell_height

            source_rectangle: tuple = (
                offset_x,
                offset_y,
                self.cell_width,
                self.cell_height,
            )

            surface.blit(
                self.image, (x, y, self.cell_width, self.cell_height), source_rectangle
            )

            x += self.cell_width

    def centre(self, surface: Surface, message: str, y):
        width = len(message) * self.cell_width
        half_width: int = surface.get_rect().width
        x = (half_width - width) / 2
        self.draw(surface, message, int(x), y)

    def to_index(self, character: str):
        return ord(character) - ord(" ")
