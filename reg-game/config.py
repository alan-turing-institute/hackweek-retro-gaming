from pathlib import Path

# APP_PATH: Path = Path('reg-game')

MENU_TITLE: str = "Regina Quest!"
MENU_FONT_IMG: Path = Path("img/fasttracker2-style_12x12.png")
MENU_BACKGROUND_PATH: Path = Path("img/2010-08-03_British_Library_exterior_02.jpg")
MENU_BACKGROUND_POSITION: tuple[int, int] = (-180, -180)
MENU_BACKGROUND_SCALE_FACTOR: float = 0.3

MENU_ITEMS: tuple[str, ...] = ("Start", "Resume", "Quit")
