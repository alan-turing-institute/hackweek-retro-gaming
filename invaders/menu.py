import pygame
from bitmapfont import BitmapFont
from framework import Game, GameState
from pygame.key import ScancodeWrapper
from pygame.locals import K_DOWN, K_SPACE, K_UP
from pygame.surface import Surface


class MainMenuState(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.play_game_state: GameState | None = None
        self.font: BitmapFont = BitmapFont("img/fasttracker2-style_12x12.png", 12, 12)
        self.index: int = 0
        self.input_tick: int = 0
        self.menu_items: list[str] = ["Start game", "Quit"]

    def set_play_state(self, state):
        self.play_game_state = state

    def update(self, game_time: int):
        keys: ScancodeWrapper = pygame.key.get_pressed()

        if keys[K_UP] or keys[K_DOWN] and self.input_tick == 0:
            self.input_tick = 250

            if keys[K_UP]:
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.menu_items) - 1

            elif keys[K_DOWN]:
                self.index += 1
                if self.index == len(self.menu_items):
                    self.index = 0
        elif self.input_tick > 0:
            self.input_tick -= game_time

        if self.input_tick < 0:
            self.input_tick = 0

        if keys[K_SPACE]:
            if self.index == 1:
                self.game.change_state(None)
            elif self.index == 0:
                self.game.change_state(self.play_game_state)

    def draw(self, surface: Surface):
        self.font.centre(surface, "Invaders! From Space", 48)
        count: int = 0
        y = surface.get_rect().height - len(self.menu_items) * 160

        for item in self.menu_items:
            item_text: str = " "

            if count == self.index:
                item_text = "> "
            item_text += item
            self.font.draw(surface, item_text, 25, y)

            y += 24
            count += 1
