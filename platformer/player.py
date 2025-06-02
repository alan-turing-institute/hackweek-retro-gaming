import pygame
from pygame.surface import Surface


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.walking_frames_r: list[Surface] = []

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
