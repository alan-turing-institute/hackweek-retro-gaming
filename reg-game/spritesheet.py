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

    def get_frames_in_row(
        self,
        row_offset: int,
        sprite_width: int,
        sprite_height: int,
        number_of_sprites: int,
        target_size: tuple[int, int],
    ) -> list[Surface]:

        sprite_surfaces: list[Surface] = [
            self.get_image(
                x=column_offset * sprite_width,
                y=sprite_height * row_offset,
                width=sprite_width,
                height=sprite_height,
            )
            for column_offset in range(0, number_of_sprites)
        ]

        return [
            pygame.transform.scale(surface, size=target_size)
            for surface in sprite_surfaces
        ]
