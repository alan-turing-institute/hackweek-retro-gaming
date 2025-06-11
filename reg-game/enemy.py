import random

import pygame
from config import N_ENEMIES, SCREEN_HEIGHT, SCREEN_WIDTH
from framework import State, StateMachine

# from enemy_statemachine import StateMachine, HackingState
from pygame.surface import Surface
from spritesheet import SpriteSheet

PLAYER_SIZE: tuple[int, int] = (96, 96)

PLAYER_SPRITESHEET_X: int = 0
PLAYER_SPRITESHEET_Y: int = 0
PLAYER_SPRITE_WIDTH: int = 48
PLAYER_SPRITE_HEIGHT: int = 48


class MaisyModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.dx = random.randint(-2, 2)
        self.dy = random.randint(-2, 2)
        self.width = 48
        self.height = 48
        self.at_terminal = False
        self.brain = StateMachine()
        self.brain.add_state(HackingState(self))
        self.brain.add_state(WanderingState(self))
        self.speed = 3


class MaisyController:
    def __init__(self):
        self.hacker_models = [
            MaisyModel(
                x=random.randint(0, SCREEN_WIDTH),
                y=random.randint(0, int(0.25 * SCREEN_HEIGHT)),
            )
            for _ in range(N_ENEMIES)
        ]
        for hacker in self.hacker_models:
            hacker.brain.set_state("wandering")

    def update(self, _game_time, *args, **kwargs):
        for hacker in self.hacker_models:
            hacker.brain.think(game_time=_game_time)


class MaisyView:
    def __init__(
        self, hacker_controller: MaisyController, sprite_sheet_path: str
    ) -> None:
        self.hackers = hacker_controller
        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path)

        self.walking_frames_left: list[Surface] = self.get_walking_frames_left()
        self.walking_frames_right: list[Surface] = self.get_walking_frames_right()

    def get_walking_frames_left(self) -> list[Surface]:
        row_offset: int = 2

        sprite_surfaces: list[Surface] = [
            self.sprite_sheet.get_image(
                x=PLAYER_SPRITESHEET_X,
                y=PLAYER_SPRITE_HEIGHT * row_offset,
                width=PLAYER_SPRITE_WIDTH,
                height=PLAYER_SPRITE_HEIGHT,
            )
        ]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def get_walking_frames_right(self) -> list[Surface]:
        row_offset: int = 3

        sprite_surfaces: list[Surface] = [
            self.sprite_sheet.get_image(
                x=PLAYER_SPRITESHEET_X,
                y=PLAYER_SPRITE_HEIGHT * row_offset,
                width=PLAYER_SPRITE_WIDTH,
                height=PLAYER_SPRITE_HEIGHT,
            )
        ]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def render(self, surface: Surface):
        for hackerview in self.hackers.hacker_models:
            if hackerview.dx >= 0:
                self.image = self.walking_frames_right[0]
            else:
                self.image = self.walking_frames_left[0]

            surface.blit(
                self.image,
                (
                    hackerview.x,
                    hackerview.y,
                    PLAYER_SPRITE_WIDTH,
                    PLAYER_SPRITE_HEIGHT,
                ),
            )


class HackingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("hacking")
        self.hacker_model = hacker_model
        self.game_time = 0

    def do_actions(self, game_time):
        self.game_time += game_time

    def check_conditions(self) -> str | None:
        print(f"At Hacking Checking conditions {self.game_time=}")
        if self.game_time > 10000:
            return "wandering"
        return None

    def entry_actions(self):
        print("Starting hacking")
        self.game_time = 0
        self.hacker_model.dx = 0
        self.hacker_model.dy = 0

    def exit_actions(self):
        self.hacker_model.at_terminal = False
        self.hacker_model.x += 40
        self.hacker_model.y += 40
        return None


class WanderingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("wandering")
        self.hacker_model = hacker_model

    def do_actions(self, game_time):
        # Change direction sometimes
        if random.random() < 0.02:
            self.hacker_model.dx = random.choice([-1, 0, 1])
            self.hacker_model.dy = random.choice([-1, 0, 1])
        if self.hacker_model.dx == 0 and self.hacker_model.dy == 0:
            self.hacker_model.dx = -1
        # Actually move
        self.hacker_model.x += self.hacker_model.dx * self.hacker_model.speed
        self.hacker_model.y += self.hacker_model.dy * self.hacker_model.speed

        # Keep maisy in bounds and bounce
        half_size = (
            int(0.5 * self.hacker_model.width),
            int(0.5 * self.hacker_model.height),
        )
        x_min = 0 - half_size[0]
        x_max = SCREEN_WIDTH - self.hacker_model.width

        y_min = 0 - half_size[1]
        y_max = SCREEN_HEIGHT - half_size[1]
        if self.hacker_model.x < x_min or self.hacker_model.x > x_max:
            self.hacker_model.dx *= -1
            if self.hacker_model.x < 0:
                self.hacker_model.x = max(
                    0, min(SCREEN_WIDTH - self.hacker_model.width, self.hacker_model.x)
                )
            else:
                self.hacker_model.x = max(
                    0, min(SCREEN_WIDTH + self.hacker_model.width, self.hacker_model.x)
                )
        if self.hacker_model.y < y_min or self.hacker_model.y > y_max:
            self.hacker_model.dy *= -1
            self.hacker_model.y = max(
                0, min(SCREEN_HEIGHT - self.hacker_model.height, self.hacker_model.y)
            )

    def check_conditions(self) -> str | None:
        print(f"At wondering {self.hacker_model.at_terminal=}")
        if self.hacker_model.at_terminal:
            return "hacking"
        return None

    def entry_actions(self):
        pass

    def exit_actions(self):
        print("Exititing wandering")


class SearchingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("searching")
        self.hacker_model = hacker_model
