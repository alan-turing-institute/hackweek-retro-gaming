from bullet import BulletController
from pygame.surface import Surface
import pygame
import random


class MaisyModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

 
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

class MaisyController:
    def __init__(self, window_width, window_height):
        self.widow_width = window_width
        self.window_height = window_height
    
        self.hackers: list[MaisyModel] = []
        self.speed = 3

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

class MaisyView:
    pass
        
class InvaderView:
    def __init__(self, swarm: SwarmController, img_path: str) -> None:
        self.image: Surface = pygame.image.load(img_path)
        self.swarm: SwarmController = swarm

    def render(self, surface: Surface):
        for invader in self.swarm.invaders:
            surface.blit(
                self.image,
                (invader.x, invader.y, 32, 32),
                (invader.anim_frame * 32, 32 * invader.alien_type, 32, 32),
            )
