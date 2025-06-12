from typing import Any, Optional

import pygame
from config import (
    SANDBOX_COUNTDOWN,
    SANDBOX_IMAGE_HEIGHT,
    SANDBOX_IMAGE_WIDTH,
    SANDBOXES_AVAILABLE,
)
from pygame.surface import Surface


class SandboxModel:
    def __init__(self, name: str | int, x: float, y: float) -> None:
        self.name: str | int = name
        self.x: float = x
        self.y: float = y
        self.hacker_at_sandbox: Optional[Any] = None


class SandboxController:
    def __init__(self) -> None:
        self.countdown: int = 0
        self.sandbox_models: list[SandboxModel] = []
        self.sandboxes_created: int = 0

    def is_sandbox_available(self) -> bool:
        return self.countdown == 0 and len(self.sandbox_models) < SANDBOXES_AVAILABLE

    def add_sandbox(self, x: float, y: float) -> None:
        self.sandbox_models.append(SandboxModel(name=self.sandboxes_created, x=x, y=y))
        self.countdown = SANDBOX_COUNTDOWN
        print(f"Added sandbox with name {self.sandboxes_created} at ({x}, {y})")
        self.sandboxes_created += 1

    def remove_sandbox(self, name: str | int) -> None:
        self.sandbox_models = [
            sandbox for sandbox in self.sandbox_models if sandbox.name != name
        ]
        self.countdown = SANDBOX_COUNTDOWN
        print(
            f"Removed sandbox {name}. Remaining sandboxes: {len(self.sandbox_models)}"
        )

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
