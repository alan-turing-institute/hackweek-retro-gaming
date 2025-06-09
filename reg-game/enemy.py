import random

import pygame
from bullet import BulletController
from pygame.surface import Surface


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
            MaisyModel(
                x=random.randint(0, self.window_width),
                y=random.randint(0, self.window_height),
            )
            for _ in range(3)
        ]
        self.speed = 3

    def update(self, _game_time):
        for hacker in self.hacker_models:
            # Change direction sometimes
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
            pygame.draw.rect(
                surface,
                hackerview.colour,
                (hackerview.x, hackerview.y, hackerview.width, hackerview.height),
            )


class InvaderModel:
    def __init__(self, x: int, y: int, alien_type: int) -> None:
        self.x: int = x
        self.y: int = y
        self.alien_type: int = alien_type
        self.anim_frame: int = 0

    def flip_frame(self):
        if self.anim_frame == 0:
            self.anim_frame = 1
        else:
            self.anim_frame = 0

    def hit(self, x: int, y: int, width: int, height: int) -> bool:
        return (
            x >= self.x
            and y >= self.y
            and x + width <= self.x + 32
            and y + height <= self.y + 32
        )


class SwarmController:
    def __init__(self, screen_width, offset_y, initial_frame_ticks) -> None:
        self.current_frame_count = initial_frame_ticks
        self.frame_count = initial_frame_ticks

        self.invaders: list[InvaderModel] = []
        self.speed_x: int = -8
        self.move_down: bool = False
        self.aliens_landed: bool = False

        self.bullets: BulletController = BulletController(200)
        self.alien_shooter: int = 3
        self.bullet_drop_time: int = 2500
        self.shoot_timer: int = self.bullet_drop_time
        self.current_shooter = 0

        for y in range(7):
            for x in range(10):
                invader: InvaderModel = InvaderModel(
                    x=160 + (x * 48) + 8, y=(y * 32) + offset_y, alien_type=y % 2
                )
                self.invaders.append(invader)

    def reset(self, offset_y, ticks) -> None:
        self.current_frame_count = ticks
        self.frame_count = ticks

        for y in range(7):
            for x in range(10):
                invader: InvaderModel = InvaderModel(
                    x=160 + (x * 48) + 8, y=(y * 32) + offset_y, alien_type=y % 2
                )
                self.invaders.append(invader)

    def update(self, game_time: int):
        self.bullets.update(game_time)
        self.frame_count -= game_time
        move_sideways: bool = True

        if self.frame_count < 0:
            if self.move_down:
                self.move_down = False
                move_sideways = False
                self.speed_x *= -1
                self.bullet_drop_time -= 250

                if self.bullet_drop_time < 1000:
                    self.bullet_drop_time = 1000

                self.current_frame_count -= 100
                if self.current_frame_count < 200:
                    self.current_frame_count = 200

                for invader in self.invaders:
                    invader.y += 32

            self.frame_count = self.current_frame_count + self.frame_count
            for invader in self.invaders:
                invader.flip_frame()

            if move_sideways:
                for invader in self.invaders:
                    invader.x += self.speed_x

            x, y, width, height = self.get_area()
            if (x <= 0 and self.speed_x < 0) or (x + width >= 800 and self.speed_x > 0):
                self.move_down = True

        self.shoot_timer -= game_time
        if self.shoot_timer <= 0:
            self.shoot_timer += self.bullet_drop_time

            self.current_shooter += self.alien_shooter
            self.current_shooter = self.current_shooter % len(self.invaders)

            shooter: InvaderModel = self.invaders[self.current_shooter]
            x = shooter.x + 9
            y = shooter.y + 16
            self.bullets.add_bullet(x, y)

    def get_area(self) -> tuple[int, int, int, int]:
        left_most: int = 2000
        right_most: int = -2000
        top_most: int = -2000
        bottom_most: int = 2000

        for invader in self.invaders:
            if invader.x < left_most:
                left_most = invader.x
            if invader.x > right_most:
                right_most = invader.x

            if invader.y < bottom_most:
                bottom_most = invader.y
            if invader.y > top_most:
                top_most = invader.y

        width: int = (right_most - left_most) + 32
        height: int = (top_most - bottom_most) + 32

        return left_most, bottom_most, width, height
