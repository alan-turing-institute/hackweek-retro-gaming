import pygame
from pygame.surface import Surface


class BitmapFont:
    def __init__(
        self, font_file: str, character_width: int, character_height: int
    ) -> None:
        """
        Handles font display.

        :param font_file: Font file.
        :param cell_width: Width of each character.
        :param cell_height: Height of each character.
        """

        self.image: Surface = pygame.image.load(font_file)
        self.character_width: int = character_width
        self.character_height: int = character_height

        image_width: int = self.image.get_rect().width
        iamge_height: int = self.image.get_rect().height

        self.columns = image_width / self.character_width
        self.rows = iamge_height / self.character_height

    def draw(self, surface: Surface, message: str, x: int, y: int):
        """
        Blits partial images of each message character to the surface.

        :param surface: The surface.
        :param message: The message.

        """
        for character in message:
            index = self.to_index(character)
            offset_x = (index % self.columns) * self.character_width
            offset_y = (index / self.columns) * self.character_height

            source_rectangle: tuple = (
                offset_x,
                offset_y,
                self.character_width,
                self.character_height,
            )

            surface.blit(
                self.image,
                (x, y, self.character_width, self.character_height),
                source_rectangle,
            )

            x += self.character_width

    def centre(self, surface: Surface, message: str, y):
        """
        Centers a message on a given line.
        """
        width: int = len(message) * self.character_width
        half_width: int = surface.get_rect().width
        x = (half_width - width) / 2
        self.draw(surface, message, int(x), y)

    def to_index(self, character: str):
        """
        Provides the index value in the bitmap font for a given character.

        :param character: The character.
        """
        return ord(character) - ord(" ")
