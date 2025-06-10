import pygame
from pygame.surface import Surface


class BulletModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def update(self, delta):
        self.y += delta


class BulletController:
    def __init__(self, speed: int) -> None:
        self.countdown: int = 0
        self.bullets: list[BulletModel] = []
        self.speed: int = speed

    def clear(self):
        self.bullets = []

    def can_fire(self) -> bool:
        return self.countdown == 0 and len(self.bullets) < 3

    def add_bullet(self, x, y):
        self.bullets.append(BulletModel(x, y))
        self.countdown = 1000

    def remove_bullet(self, bullet: BulletModel):
        self.bullets.remove(bullet)

    def update(self, game_time, *args, **kwargs) -> None:
        kill_list: list[BulletModel] = []

        if self.countdown > 0:
            self.countdown -= game_time
        else:
            self.countdown = 0

        for bullet in self.bullets:
            bullet.update(self.speed * (game_time / 1000.0))
            if bullet.y < 0:
                kill_list.append(bullet)

        for bullet in kill_list:
            self.remove_bullet(bullet)


class BulletView:
    def __init__(self, bullet_controller: BulletController, img_path) -> None:
        self.bullet_controller: BulletController = bullet_controller
        self.image = pygame.image.load(img_path)

    def render(self, surface: Surface):
        for bullet in self.bullet_controller.bullets:
            surface.blit(self.image, (bullet.x, bullet.y, 8, 8))
