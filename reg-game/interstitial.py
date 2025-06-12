from bitmapfont import BitmapFont
from config import MENU_FONT_IMG
from framework import Game, GameState
from pygame import Surface
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MENU_BACKGROUND_PATH,
    MENU_BACKGROUND_POSITION,
)
import pygame
from pygame.image import load
from pathlib import Path


class InterstitialState(GameState):
    def __init__(
        self,
        game: Game,
        message: str,
        wait_time_ms: int,
        next_state: GameState | None,
        background_path: Path | str = MENU_BACKGROUND_PATH,
    ) -> None:
        """
        :param game: Game instance.
        """
        super().__init__(game)

        self.next_state: GameState | None = next_state
        self.font: BitmapFont = BitmapFont(str(MENU_FONT_IMG), 12, 12)
        self.message: str = message
        self.wait_timer: int = wait_time_ms

        self.background: Surface = load(background_path).convert()
        self.background = pygame.transform.scale(
            self.background, size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def update(self, game_time: int, *args, **kwargs):
        """
        Waits until the timer runs down. When timer reaches zero, game moves to the next state.

        :param game_time: Game time.
        """
        self.wait_timer -= game_time
        if self.wait_timer < 0:
            self.game.change_state(self.next_state)

    def draw(self, surface: Surface):

        surface.blit(self.background, MENU_BACKGROUND_POSITION)

        messages = self.message.split("\n")
        if len(messages) > 1:
            for i, message in enumerate(messages):
                self.font.centre(
                    surface, message, -40 + surface.get_rect().height / 2 + i * 20
                )
        else:
            self.font.centre(surface, self.message, surface.get_rect().height / 2)
