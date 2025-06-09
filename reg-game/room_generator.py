
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from random import randint

terminal_img = "img/CommTerminal.png"

def generate_room(n_terminals, room_size=(SCREEN_WIDTH, SCREEN_HEIGHT)):

    terminal_width = 32
    terminal_height = 32

    max_y = SCREEN_HEIGHT - terminal_height
    min_y = 0 + terminal_height
    max_x = SCREEN_WIDTH - terminal_width
    min_x = 0 + terminal_width

    terminals = {}
    for i in range(n_terminals):
        terminal_name = f"Terminal {i + 1 }"
        terminal_location = (
            randint(min_x, max_x),
            randint(min_y, max_y)
        )
        terminals[terminal_name] = terminal_location

    return terminals

print(generate_room(2))