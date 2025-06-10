from config import SANDBOXES_AVAILABLE
import pygame
from pygame.surface import Surface
from config import SANDBOX_IMAGE_WIDTH, SANDBOX_IMAGE_HEIGHT, SANDBOX_COUNTDOWN


class SandboxModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class SandboxController:

    def __init__(self) -> None:
        self.countdown: int = 0
        self.sandbox_models: list[SandboxModel] = []

    def is_sandbox_available(self) -> bool:
        return self.countdown == 0 and len(self.sandbox_models) < SANDBOXES_AVAILABLE

    def add_sandbox(self, x, y):
        self.sandbox_models.append(SandboxModel(x=x, y=y))
        self.countdown = SANDBOX_COUNTDOWN

    def update(self, game_time: int, *args, **kwargs) -> None:
        if self.countdown > 0:
            self.countdown -= game_time
        else:
            self.countdown = 0


class SandboxView:

    def __init__(self, sandbox_controller: SandboxController, image_path: str) -> None:
        self.sandbox_controller: SandboxController = sandbox_controller
        self.image = pygame.image.load(image_path)

    def render(self, surface: Surface) -> None:
        for sandbox_model in self.sandbox_controller.sandbox_models:
            surface.blit(
                self.image,
                (
                    sandbox_model.x,
                    sandbox_model.y,
                    SANDBOX_IMAGE_WIDTH,
                    SANDBOX_IMAGE_HEIGHT,
                ),
            )
