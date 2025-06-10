import random

import pygame
from bullet import BulletController
from config import SCREEN_HEIGHT, SCREEN_WIDTH

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
            for _ in range(3)
        ]
        for hacker in self.hacker_models:
            hacker.brain.set_state("wandering_state")

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

    def update(self, game_time: int, *args, **kwargs):
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


class State:
    def __init__(self, name: str):
        self.name: str = name

    def do_actions(self, game_time):
        pass

    def check_conditions(self) -> str | None:
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine:
    def __init__(self) -> None:
        self.states: dict[str, State] = {}
        self.active_state: State | None = None

    def add_state(self, state: "State"):
        self.states[state.name] = state

    def think(self, game_time) -> None:
        if self.active_state is None:
            return

        self.active_state.do_actions(game_time)

        new_state_name: str | None = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name: str):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class HackingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("hacking_state")
        self.hacker_model = hacker_model
        self.game_time = 0

    def do_actions(self, game_time):
        # print(f"Doing actions {game_time}")
        self.game_time += game_time
        # print(self.game_time)

    def check_conditions(self) -> str | None:
        # print(f"Checking conditions {self.game_time}")
        if self.game_time > 2000:
            return "wandering_state"

        return None

    def entry_actions(self):
        print("Check conditions")

    def exit_actions(self):
        # print("Exit")
        pass


class WanderingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("wandering_state")
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
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        print("Exit")


class SearchingState(State):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("wandering_state")
        self.hacker_model = hacker_model
