import sys

import pygame
from pygame import Color
from pygame.locals import QUIT
from pygame.surface import Surface
from pygame.time import Clock


class GameState:
    def __init__(self, game: "Game") -> None:
        """
        Represents a game state, and manages a specific game function

        :param game: The game instance.
        """
        self.game: "Game" = game

    def on_enter(self, previous_state: "GameState | None"):
        """
        Called by the game instance when entering a state for the first time.

        :param previous_state: The previous state.
        :returns: None
        """
        pass

    def on_exit(self):
        """
        Called by the game instance when leaving the state. Useful for cleanup and any other tasks before leaving the state.

        :param None
        :returns: None
        """
        pass

    def update(self, game_time: int, *args, **kwargs):
        """
        Called by the game instance to update the state.

        :param game_time: Game time in milliseconds since the last call.
        :returns: None
        """
        pass

    def draw(self, surface: Surface):
        """
        Called by the game instance to draw the state.

        :param surface: The current drawing surface.
        :returns: None
        """
        pass


class Game:
    def __init__(self, game_name: str, width: int, height: int):
        """
        Manages the game states, that determine what's on screen and that update over time.

        :param game_name: Name of the game. It's shown in the window's title bar.
        :returns: None
        """
        pygame.init()
        pygame.display.set_caption(game_name)

        self.fps_clock: Clock = Clock()
        self.main_window: Surface = pygame.display.set_mode((width, height))
        self.background: Color = Color(0, 0, 0)
        self.current_state: GameState | None = None

    def change_state(self, new_state: GameState | None):
        """
        Transitions from one state to another. It will also call on_exit() on the existing state.

        :param new_state: If provided, its on_enter() method will be called. If None, the game will terminate.
        :returns: None
        """
        if self.current_state is not None:
            self.current_state.on_exit()

        if new_state is None:
            pygame.quit()
            sys.exit()

        old_state = self.current_state
        self.current_state = new_state
        new_state.on_enter(old_state)

    def run(self, initial_state: GameState | None):
        """
        Main game loop. Handles event management, state update and display.
        """
        self.change_state(initial_state)

        while True:
            # position of a mouse click (needed for some games which rely on mouse click inputs)
            # pygame.event.get clears the event queue so we would miss events if we read them in the update
            pos = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse click
                        pos = event.pos

            game_time: int = self.fps_clock.get_time()
            if self.current_state is not None:
                self.current_state.update(game_time, pos)

            self.main_window.fill(self.background)

            if self.current_state is not None:
                self.current_state.draw(self.main_window)

            pygame.display.update()
            self.fps_clock.tick(30)
