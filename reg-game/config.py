from pathlib import Path

# APP_PATH: Path = Path('reg-game')

MENU_TITLE: str = "Regina Quest!"
MENU_FONT_IMG: Path = Path("img/fasttracker2-style_12x12.png")
MENU_BACKGROUND_PATH: Path = Path("img/british-library-14880.jpg")
MENU_BACKGROUND_POSITION: tuple[int, int] = (0, 0)
MENU_BACKGROUND_SCALE_FACTOR: float = 1.0

MENU_ITEMS: tuple[str, ...] = ("Start", "Resume", "Quit")

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

PLAYER_SIZE: tuple[int, int] = (64, 64)
PLAYER_SPRITE_SHEET_PATH: str = "img/24by24ModernRPGGuy.png"
PLAYER_SPRITE_HEIGHT: int = 24
PLAYER_SPRITE_WIDTH: int = 24

SANDBOX_IMAGE_PATH: str = "img/moving_pikes.png"
SANDBOXES_AVAILABLE: int = 3
SANDBOX_IMAGE_WIDTH: int = 32
SANDBOX_IMAGE_HEIGHT: int = 32
SANDBOX_COUNTDOWN: int = 1000

UNHACKABLE_COUNTDOWN: int = 3000


PLAYER_NUMBER_OF_SPRITES: int = 4

TERMINAL_SIZE: tuple[int, int] = (64, 64)
NUMBER_OF_TERMINALS: int = 3
TERMINAL_SPRITE_SHEET: str = "img/icon1.png"
TERMINAL_IMAGE_SERVER: str = "img/server.png"
TERMINAL_IMAGE_COMPUTER_ON: str = "img/computer2.png"
TERMINAL_IMAGE_COMPUTER_OFF: str = "img/computer1.png"


TERMINAL_IMAGE_WIDTH: int = 38
TERMINAL_IMAGE_HEIGHT: int = 38

LIVES_SPRITE_SHEET_PATH: str = "img/male_ivory_lizard_head.png"
LIVES_SPRITE_WIDTH: int = 64
LIVES_SPRITE_HEIGHT: int = 64

LIVES_MESSAGE_X: int = 160
LIVES_MESSAGE_Y: int = 30

N_ENEMIES: int = 3
