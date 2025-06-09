import random
import sys

import pygame

pygame.init()

# Window settings
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Character")

# Character settings
CHAR_SIZE = 20
char_x, char_y = WIDTH // 2, HEIGHT // 2
CHAR_COLOR = (0, 128, 255)
SPEED = 5


# ---------
class MaisyModel:
    def __init__(self, x: int, y: int, win: pygame.surface) -> None:
        self.x: int = x
        self.y: int = y
        self.win = win
        self.width = 40
        self.height = 20
        self.dx = 0
        self.dy = 0
        self.win_width = self.win.get_width()
        self.win_height = self.win.get_height()

    def move(self):
        """Move a random direction and stay in bounds"""
        self.speed = 3
        # Change direction sometimes
        if random.random() < 0.02:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            if self.dx == 0 and self.dy == 0:
                self.dx = -1
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Keep maisy in bounds and bounce
        if self.x < 0 or self.x > self.win_width - self.width:
            self.dx *= -1
            self.x = max(0, min(self.win_width - self.width, self.x))
        if self.y < 0 or self.y > self.win_height - self.height:
            self.dy *= -1
            self.y = max(0, min(self.win_height - self.height, self.y))

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.width, self.height))


# ---------


# Create maisy instance
maisy = MaisyModel(
    random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), win=WIN
)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        char_x -= SPEED
    if keys[pygame.K_RIGHT]:
        char_x += SPEED
    if keys[pygame.K_UP]:
        char_y -= SPEED
    if keys[pygame.K_DOWN]:
        char_y += SPEED

    # Move maisy
    maisy.move(WIDTH, HEIGHT)

    # Keep character in bounds
    char_x = max(0, min(WIDTH - CHAR_SIZE, char_x))
    char_y = max(0, min(HEIGHT - CHAR_SIZE, char_y))

    # Drawing
    WIN.fill((30, 30, 30))  # Background color
    pygame.draw.rect(WIN, CHAR_COLOR, (char_x, char_y, CHAR_SIZE, CHAR_SIZE))
    maisy.draw(WIN)
    pygame.display.flip()

pygame.quit()
sys.exit()
