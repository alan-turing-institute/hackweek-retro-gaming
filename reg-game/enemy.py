import random

import pygame
from config import ENEMY_SPEED, N_ENEMIES, PLAYER_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from framework import EntityState, EntityStateMachine

# from enemy_statemachine import StateMachine, HackingState
from pygame.surface import Surface
from sandbox import SandboxController, SandboxModel
from spritesheet import SpriteSheet
from terminals import TerminalModel

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
        self.active_terminal: None | TerminalModel = None
        self.active_sandbox: None | SandboxModel = None
        self.active_sandbox_name: str = ("",)
        self.sandbox_controller: None | SandboxController = None
        self.brain = EntityStateMachine()
        self.brain.add_state(HackingState(self))
        self.brain.add_state(WanderingState(self))
        self.brain.add_state(SandboxState(self))
        self.speed = ENEMY_SPEED


class MaisyController:
    def __init__(self):
        self.hacker_models = [
            MaisyModel(
                x=SCREEN_WIDTH / 2 + random.randint(-100, 100),
                y=SCREEN_HEIGHT / 2 + random.randint(-100, 100),
            )
            for _ in range(N_ENEMIES)
        ]
        for hacker in self.hacker_models:
            hacker.brain.set_state("wandering")

    def update(self, _game_time, *args, **kwargs):
        for hacker in self.hacker_models:
            # print(f"{hacker.brain.active_state.name=}")
            hacker.brain.think(game_time=_game_time)


class MaisyView:
    def __init__(
        self, hacker_controller: MaisyController, sprite_sheet_path: str
    ) -> None:
        self.hackers = hacker_controller
        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path)
        # agents_count: int = N_ENEMIES + 1 # assuming enemies + hero

        self.walking_frames_left: list[Surface] = self.get_walking_frames_left()
        self.walking_frames_right: list[Surface] = self.get_walking_frames_right()

        self.facing_left: Surface = self.get_left_facing()
        self.facing_right: Surface = self.get_right_facing()
        # self.moving_frames_right: list[Surface] = self.sprite_sheet.get_frames_in_row(
        #     row_offset=2,
        #     sprite_width=ENEMY_SPRITE_WIDTH,
        #     sprite_height=ENEMY_SPRITE_HEIGHT,
        #     number_of_sprites=agents_count,            target_size=ENEMY_SIZE,
        # )
        #
        # self.moving_frames_left: list[Surface] = self.sprite_sheet.get_frames_in_row(
        #     row_offset=3,
        #     sprite_width=ENEMY_SPRITE_WIDTH,
        #     sprite_height=ENEMY_SPRITE_HEIGHT,
        #     number_of_sprites=agents_count,
        #     target_size=ENEMY_SIZE,
        # )
        #
        # self.moving_frames_up: list[Surface] = self.sprite_sheet.get_frames_in_row(
        #     row_offset=0,
        #     sprite_width=ENEMY_SPRITE_WIDTH,
        #     sprite_height=ENEMY_SPRITE_HEIGHT,
        #     number_of_sprites=agents_count,
        #     target_size=ENEMY_SIZE,
        # )
        #
        # self.moving_frames_down: list[Surface] = self.sprite_sheet.get_frames_in_row(
        #     row_offset=1,
        #     sprite_width=ENEMY_SPRITE_WIDTH,
        #     sprite_height=ENEMY_SPRITE_HEIGHT,
        #     number_of_sprites=agents_count,
        #     target_size=ENEMY_SIZE,
        # )
        # self.image: Surface = self.moving_frames_right[0]

    # def render(self, surface: Surface):
    #     list_index: int = 0
    #     if self.player_controller.player_model.direction == "RIGHT":
    #         list_index = int(self.player_controller.player_model.x) % len(
    #             self.moving_frames_right
    #         )
    #         self.image = self.moving_frames_right[list_index]
    #     elif self.player_controller.player_model.direction == "LEFT":
    #         list_index = int(self.player_controller.player_model.x) % len(
    #             self.moving_frames_left
    #         )
    #         self.image = self.moving_frames_left[list_index]
    #     elif self.player_controller.player_model.direction == "UP":
    #         list_index = int(self.player_controller.player_model.y) % len(
    #             self.moving_frames_up
    #         )
    #         self.image = self.moving_frames_up[list_index]
    #     elif self.player_controller.player_model.direction == "DOWN":
    #         list_index = int(self.player_controller.player_model.y) % len(
    #             self.moving_frames_down
    #         )
    #         self.image = self.moving_frames_down[list_index]
    #
    #     surface.blit(
    #         self.image,
    #         (
    #             self.player_controller.player_model.x,
    #             self.player_controller.player_model.y,
    #             PLAYER_SPRITE_WIDTH,
    #             PLAYER_SPRITE_HEIGHT,
    #         ),
    #     )

    def get_left_facing(self) -> Surface:
        sprite_surface = self.sprite_sheet.get_image(512, 0, 512, 512)
        return pygame.transform.scale(sprite_surface, size=PLAYER_SIZE)

    def get_right_facing(self) -> Surface:
        sprite_surface = self.sprite_sheet.get_image(0, 0, 512, 512)
        return pygame.transform.scale(sprite_surface, size=PLAYER_SIZE)

    def get_walking_frames_left(self) -> list[Surface]:
        sprite_surfaces: list[Surface] = [self.sprite_sheet.get_image(512, 0, 512, 512)]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def get_walking_frames_right(self) -> list[Surface]:
        sprite_surfaces: list[Surface] = [self.sprite_sheet.get_image(0, 0, 512, 512)]

        return [
            pygame.transform.scale(surface, size=PLAYER_SIZE)
            for surface in sprite_surfaces
        ]

    def render(self, surface: Surface):
        for hacker in self.hackers.hacker_models:
            if hacker.dx >= 0:
                self.image = self.facing_right
                # self.image = self.walking_frames_right[0]
            else:
                # self.image = self.walking_frames_left[0]
                self.image = self.facing_left

            surface.blit(
                self.image,
                (
                    hacker.x,
                    hacker.y,
                    PLAYER_SPRITE_WIDTH,
                    PLAYER_SPRITE_HEIGHT,
                ),
            )


class HackingState(EntityState):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("hacking")
        self.hacker_model = hacker_model
        self.game_time = 0

    def do_actions(self, game_time):
        self.game_time += game_time
        # print(self.hacker_model.active_terminal.state_machine.active_state.name)

    def check_conditions(self) -> str | None:
        if self.game_time > 10000:
            return "wandering"
        if self.hacker_model.active_terminal is None:
            return "wandering"
        return None

    def entry_actions(self):
        # print("Starting hacking")
        self.game_time = 0
        self.hacker_model.dx = 0
        self.hacker_model.dy = 0

    def exit_actions(self):
        # self.hacker_model.active_terminal = None
        self.hacker_model.x = SCREEN_WIDTH / 2
        self.hacker_model.y = SCREEN_HEIGHT / 2
        self.hacker_model.dx = random.choice([-3, 3])
        self.hacker_model.dy = random.choice([-3, 3])
        return None


class WanderingState(EntityState):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("wandering")
        self.hacker_model = hacker_model
        # self.terminals = terminals

    def check_x_boundary(self):
        return (
            self.hacker_model.x > (SCREEN_WIDTH - int(0.5 * PLAYER_SPRITE_WIDTH) - 5)
            or self.hacker_model.x < 5
        )

    def check_y_boundary(self):
        return self.hacker_model.y < 5 or self.hacker_model.y > (
            SCREEN_HEIGHT - int(0.5 * PLAYER_SPRITE_HEIGHT) - 5
        )

    def do_actions(self, game_time):
        # Change direction sometimes
        if random.random() < 0.02:
            self.hacker_model.dx = random.choice([-1, 1])
            self.hacker_model.dy = random.choice([-1, 1])
        # Actually move
        self.hacker_model.x += self.hacker_model.dx * self.hacker_model.speed
        self.hacker_model.y += self.hacker_model.dy * self.hacker_model.speed

        # Keep maisy in bounds and bounce
        if self.check_x_boundary():
            self.hacker_model.dx *= -1

        if self.check_y_boundary():
            self.hacker_model.dy *= -1

        # half_size = (
        #     int(0.5 * self.hacker_model.width),
        #     int(0.5 * self.hacker_model.height),
        # )
        # x_min = 0 - half_size[0]
        # x_max = SCREEN_WIDTH - self.hacker_model.width

        # y_min = 0 - half_size[1]
        # y_max = SCREEN_HEIGHT - half_size[1]
        # if self.hacker_model.x < x_min or self.hacker_model.x > x_max:
        #     self.hacker_model.dx *= -1
        #     if self.hacker_model.x < 0:
        #         self.hacker_model.x = max(
        #             0, min(SCREEN_WIDTH - self.hacker_model.width, self.hacker_model.x)
        #         )
        #     else:
        #         self.hacker_model.x = max(
        #             0, min(SCREEN_WIDTH + self.hacker_model.width, self.hacker_model.x)
        #         )
        # if self.hacker_model.y < y_min or self.hacker_model.y > y_max:
        #     self.hacker_model.dy *= -1
        #     self.hacker_model.y = max(
        #         0, min(SCREEN_HEIGHT - self.hacker_model.height, self.hacker_model.y)
        #     )

        # print(f"Positions = {self.hacker_model.x=}, {self.hacker_model.y=}")

    def check_conditions(self) -> str | None:
        # print(f"At wandering {self.hacker_model.at_terminal=}")

        # TODO: Remove later
        # if self.hacker_model.active_terminal is not None:
        #     print(f"Hacker ->{self.hacker_model.active_terminal=}")
        #     print(
        #         f"Hacker ->{self.hacker_model.active_terminal.state_machine.active_state.name=}"
        #     )

        if (
            self.hacker_model.active_terminal is not None
            and self.hacker_model.active_terminal.hacker_at_terminal
            == self.hacker_model
        ):
            return "hacking"
        if self.hacker_model.active_sandbox is not None:
            self.hacker_model.active_sandbox_name = (
                self.hacker_model.active_sandbox.name
            )
            return "in_sandbox"
        return None

    def entry_actions(self):
        # print("Entered wandering")
        print(
            f"{self.hacker_model.dx=}, {self.hacker_model.dy=}, {self.hacker_model.speed}"
        )
        pass

    def exit_actions(self):
        # print("Exititing wandering")
        pass


class SandboxState(EntityState):
    def __init__(self, hacker_model: "MaisyModel"):
        super().__init__("in_sandbox")
        self.hacker_model = hacker_model

    def do_actions(self, game_time):
        self.game_time += game_time

    def check_conditions(self) -> str | None:
        if self.game_time > 10000:
            return "wandering"
        return None

    def entry_actions(self):
        self.game_time = 0
        self.hacker_model.dx = 0
        self.hacker_model.dy = 0

    def exit_actions(self):
        self.hacker_model.x += 40
        self.hacker_model.y += 40
        self.hacker_model.sandbox_controller.remove_sandbox(
            self.hacker_model.active_sandbox_name
        )
        self.hacker_model.active_sandbox = None
        self.hacker_model.active_sandbox_name = ""


class SearchingState(EntityState):
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
