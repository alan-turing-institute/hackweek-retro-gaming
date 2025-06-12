from dataclasses import dataclass
from pathlib import Path

# APP_PATH: Path = Path('reg-game')


@dataclass
class Attribution:
    local_path: Path
    url: str | None = None
    license: str | None = None
    notes: str = ""


british_library: Attribution = Attribution(
    url="https://imagesonline.bl.uk/asset/14880/",
    license="British Library",
    local_path=Path("img/british-library-14880.jpg"),
)

regina: Attribution = Attribution(
    url="https://www.deviantart.com/gogoat1/art/Gym-Leader-Cheryl-OW-sprite-906059354",
    license="https://creativecommons.org/licenses/by-nc-nd/3.0",
    local_path=Path("img/gym_leader_cheryl_transparent_background.png"),
    notes="Modified for transperent background via GIMP",
)

enemy: Attribution = Attribution(
    url="https://opengameart.org/content/modern-rpg-guy",
    license="http://creativecommons.org/publicdomain/zero/1.0/",
    local_path=Path("img/24by24ModernRPGGuy.png"),
)

MENU_TITLE: str = "Regina Quest!"
MENU_FONT_IMG: Path = Path("img/fasttracker2-style_12x12.png")
MENU_BACKGROUND_PATH: Path = british_library.local_path
MENU_BACKGROUND_POSITION: tuple[int, int] = (0, 0)
MENU_BACKGROUND_SCALE_FACTOR: float = 1.0

MENU_ITEMS: tuple[str, ...] = ("Start", "Resume", "Quit")

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

PLAYER_SIZE: tuple[int, int] = (64, 64)
PLAYER_SPRITE_SHEET_PATH: str = str(regina.local_path)
PLAYER_SPRITE_HEIGHT: int = 128
PLAYER_SPRITE_WIDTH: int = 128
PLAYER_FACING_RIGHT_OFFSET: int = 2
PLAYER_FACING_LEFT_OFFSET: int = 1
PLAYER_FACING_UP_OFFSET: int = 3
PLAYER_FACING_DOWN_OFFSET: int = 0

NME_SIZE: tuple[int, int] = (64, 64)
NME_SPRITE_SHEET_PATH: str = str(enemy.local_path)
NME_SPRITE_HEIGHT: int = 128
NME_SPRITE_WIDTH: int = 128
NME_FACING_RIGHT_OFFSET: int = 2
NME_FACING_LEFT_OFFSET: int = 1
NME_FACING_UP_OFFSET: int = 3
NME_FACING_DOWN_OFFSET: int = 0

SANDBOX_IMAGE_PATH: str = "img/moving_pikes.png"
SANDBOXES_AVAILABLE: int = 3
SANDBOX_IMAGE_WIDTH: int = 32
SANDBOX_IMAGE_HEIGHT: int = 32
SANDBOX_COUNTDOWN: int = 1000

UNHACKABLE_COUNTDOWN: int = 3000
HACKING_COUNTDOWN: int = 10000  # Should be 10000
FIXING_SCORE: int = 10


PLAYER_NUMBER_OF_SPRITES: int = 4
NME_NUMBER_OF_SPRITES: int = 4

TERMINAL_SIZE: tuple[int, int] = (64, 64)
NUMBER_OF_TERMINALS: int = 1  # TODO: Edit later.
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

N_ENEMIES: int = 1
ENEMY_SPEED: int = 3  # TODO: Edit later

# ENEMY_SIZE: tuple[int, int] = (96, 96)
ENEMY_SPRITESHEET_X: int = 0
ENEMY_SPRITESHEET_Y: int = 0
# ENEMY_SPRITE_WIDTH: int = 48
# ENEMY_SPRITE_HEIGHT: int = 48
# ENEMY_SIZE: tuple[int, int] = (48, 48)
ENEMY_SIZE: tuple[int, int] = (96, 96)
ENEMY_SPRITE_SHEET_PATH: str = str(enemy.local_path)
ENEMY_SPRITE_HEIGHT: int = 128
ENEMY_SPRITE_WIDTH: int = 128
ENEMY_FACING_RIGHT_OFFSET: int = 2
ENEMY_FACING_LEFT_OFFSET: int = 3
ENEMY_FACING_UP_OFFSET: int = 0
ENEMY_FACING_DOWN_OFFSET: int = 1
