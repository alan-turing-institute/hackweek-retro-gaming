import sys

import moderngl
import pygame
from glshaders import glContext
from pygame import Color
from pygame.locals import QUIT
from pygame.surface import Surface
from pygame.time import Clock
from sounds import MusicPlayer


class EntityState:
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


class EntityStateMachine:
    def __init__(self) -> None:
        self.states: dict[str, EntityState] = {}
        self.active_state: EntityState | None = None

    def add_state(self, state: "EntityState"):
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
        # see https://stackoverflow.com/questions/76151435/creating-a-context-utilizing-moderngl-for-pygame
        # need to do some set up work for OpenGL context creation on Mac
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

        self.fps_clock: Clock = Clock()
        self.main_window: Surface = pygame.display.set_mode((width, height))
        self.gl_screen: Surface = pygame.display.set_mode(
            (width, height), pygame.OPENGL | pygame.DOUBLEBUF
        )
        self.ctx: glContext = glContext()
        self.background: Color = Color(0, 0, 0)
        self.current_state: GameState | None = None
        self.music_player: MusicPlayer = MusicPlayer()

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
        print(type(new_state).__name__)
        if type(new_state).__name__ == "MainMenuState":
            self.music_player.start("sound/reggame-v2.mp3")
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

            frame_tex = self.surf_to_texture(self.main_window)
            frame_tex.use(0)
            self.ctx.render(type(self.current_state).__name__)

            pygame.display.flip()
            frame_tex.release()
            self.fps_clock.tick(30)

    def surf_to_texture(self, surface: Surface):
        """
        Converts a pygame surface to a moderngl texture.

        :param surface: The pygame surface to convert.
        :returns: A moderngl texture.
        """
        texture = self.ctx.ctx.texture(surface.get_size(), 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = "BGRA"
        texture.write(surface.get_view("1"))
        return texture
