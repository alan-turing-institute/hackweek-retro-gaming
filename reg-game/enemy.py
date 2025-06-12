import random
from dataclasses import dataclass

import pygame
from config import (
    ENEMY_FACING_DOWN_OFFSET,
    ENEMY_FACING_LEFT_OFFSET,
    ENEMY_FACING_RIGHT_OFFSET,
    ENEMY_FACING_UP_OFFSET,
    ENEMY_SIZE,
    ENEMY_SPRITE_HEIGHT,
    ENEMY_SPRITE_WIDTH,
    N_ENEMIES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from framework import State, StateMachine
from pygame.surface import Surface
from regplayer import MovingFrames
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
        self.width = ENEMY_SPRITE_WIDTH
        self.height = ENEMY_SPRITE_HEIGHT
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


@dataclass
class MaisyMovingFrames(MovingFrames):
    character_right_offset: int = ENEMY_FACING_RIGHT_OFFSET
    character_left_offset: int = ENEMY_FACING_LEFT_OFFSET
    character_up_offset: int = ENEMY_FACING_UP_OFFSET
    character_down_offset: int = ENEMY_FACING_DOWN_OFFSET

    character_size: tuple[int, int] = ENEMY_SIZE
    character_height: int = ENEMY_SPRITE_HEIGHT
    character_width: int = ENEMY_SPRITE_WIDTH


class MaisyView:
    def __init__(
        self, hacker_controller: MaisyController, sprite_sheet_path: str
    ) -> None:
        self.hackers = hacker_controller
        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path)
        # agents_count: int = N_ENEMIES + 1 # assuming enemies + hero
        self.moving_frames = MaisyMovingFrames(sprite_sheet=self.sprite_sheet)

    def render(self, surface: Surface):
        for hackerview in self.hackers.hacker_models:
            list_index: int = 0
            if hackerview.dx >= 0:
                list_index = int(hackerview.x) % len(self.moving_frames.right)
                self.image = self.moving_frames.right[list_index]
            elif hackerview.dy >= 0:
                list_index = int(hackerview.y) % len(self.moving_frames.up)
                self.image = self.moving_frames.up[list_index]
            elif hackerview.dx < 0:
                list_index = int(hackerview.x) % len(self.moving_frames.left)
                self.image = self.moving_frames.left[list_index]
            else:
                list_index = int(hackerview.y) % len(self.moving_frames.down)
                self.image = self.moving_frames.down[0]

            self.image = pygame.transform.scale(self.image, ENEMY_SIZE)
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
        # print(f"At Hacking Checking conditions {self.game_time=}")
        if self.game_time > 10000:
            # print("TIME UP")
            return "wandering"
        return None

    def entry_actions(self):
        # print("Starting hacking")
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
        # self.terminals = terminals

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
        # print(f"At wandering {self.hacker_model.at_terminal=}")
        if self.hacker_model.at_terminal:
            return "hacking"
        return None

    def entry_actions(self):
        pass

    def exit_actions(self):
        # print("Exititing wandering")
        pass


class SearchingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("searching")
        self.hacker_model = hacker_model

    def do_actions(self, game_time):
        pass

    def check_conditions(self) -> str | None:
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass
