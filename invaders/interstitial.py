from bitmapfont import BitmapFont
from framework import Game, GameState
from pygame import Surface


class InterstitialState(GameState):
    def __init__(
        self, game: Game, message: str, wait_time_ms: int, next_state: GameState | None
    ) -> None:
        """
        :param game: Game instance.
        """
        super().__init__(game)

        self.next_state: GameState | None = next_state
        self.font: BitmapFont = BitmapFont("img/fasttracker2-style_12x12.png", 12, 12)
        self.message: str = message
        self.wait_timer: int = wait_time_ms

    def update(self, game_time: int, *args, **kwargs):
        """
        Waits until the timer runs down. When timer reaches zero, game moves to the next state.

        :param game_time: Game time.
        """
        self.wait_timer -= game_time
        if self.wait_timer < 0:
            self.game.change_state(self.next_state)

    def draw(self, surface: Surface):
        self.font.centre(surface, self.message, surface.get_rect().height / 2)
