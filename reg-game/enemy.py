from pygame.surface import Surface
import pygame
import random

class MaisyModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = 40
        self.height = 20
        self.colour = (0, 128, 255)


class MaisyController:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
    
        self.hacker_models = [
            MaisyModel(x=random.randint(0,self.window_width),
                       y = random.randint(0, self.window_height))
                       for _ in range(3)
        ]
        self.speed = 3

    def update(self, _game_time):
        for hacker in self.hacker_models:
            # Change direction sometimes
            if random.random() < 0.02:
                hacker.dx = random.choice([-1, 0, 1])
                hacker.dy = random.choice([-1, 0, 1])
                if hacker.dx == 0 and hacker.dy == 0:
                    hacker.dx = -1
            hacker.x += hacker.dx * self.speed
            hacker.y += hacker.dy * self.speed

            # Keep maisy in bounds and bounce
            if hacker.x < 0 or hacker.x > self.window_width - hacker.width:
                hacker.dx *= -1
                hacker.x = max(0, min(self.window_width - hacker.width, hacker.x))
            if hacker.y < 0 or hacker.y > self.window_height - hacker.height:
                hacker.dy *= -1
                hacker.y = max(0, min(self.window_height - hacker.height, hacker.y))


class MaisyView:
    def __init__(self, hacker_controller: MaisyController) -> None:
        self.hackers = hacker_controller
    
    def render(self, surface: Surface):
        for hackerview in self.hackers.hacker_models:
            pygame.draw.rect(surface, hackerview.colour, (hackerview.x, hackerview.y, hackerview.width, hackerview.height))


