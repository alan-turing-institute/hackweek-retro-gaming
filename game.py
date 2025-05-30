import pygame
from pygame.time import Clock
from pygame.surface import Surface
from pygame.locals import QUIT
from pygame import Color
import sys


class GameState:
    def __init__(self, game: "Game") -> None:
        self.game: "Game" = game

    def on_enter(self, previous_state: "GameState | None"):
        pass

    def on_exit(self):
        pass

    def update(self, game_time: int):
        pass

    def draw(self, surface: Surface):
        pass


class Game:
    def __init__(self, game_name: str, width: int, height: int):
        pygame.init()
        pygame.display.set_caption(game_name)

        self.fps_clock: Clock = Clock()
        self.main_window: Surface = pygame.display.set_mode((width, height))
        self.background: Color = Color(0, 0, 0)
        self.current_state: GameState | None = None

    def change_state(self, new_state: GameState | None):
        if self.current_state is not None:
            self.current_state.on_exit()

        if new_state is None:
            pygame.quit()
            sys.exit()

        old_state = self.current_state
        self.current_state = new_state
        new_state.on_enter(old_state)

    def run(self, initial_state: GameState | None):
        self.change_state(initial_state)

        while True:
            for event in pygame.event.get():
                if event == QUIT:
                    pygame.quit()
                    sys.exit()

                game_time: int = self.fps_clock.get_time()
                if self.current_state is not None:
                    self.current_state.update(game_time)

                self.main_window.fill(self.background)

                if self.current_state is not None:
                    self.current_state.draw(self.main_window)

                pygame.display.update()
                self.fps_clock.tick(30)
