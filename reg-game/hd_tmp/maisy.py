from pygame.surface import Surface
import pygame
import random

# Maisy is a hacker putting malware onto the terminals in the power station
class MaisyModel:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.size: int = 20  # Add a size for drawing

    def move(self, width=640, height=480):
        """Move a random direction and stay in bounds"""
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        speed = 3
        self.x += dx * speed
        self.y += dy * speed
        # Keep in bounds
        self.x = max(0, min(width - self.size, self.x))
        self.y = max(0, min(height - self.size, self.y))

    def draw(self, surface: Surface):
        pygame.draw.rect(surface, (255, 255, 0), (self.x, self.y, self.size, self.size))