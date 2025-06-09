import pygame
from pygame.surface import Surface
from pygame.time import Clock
import sys

SCREEN_SIZE: tuple[int, int] = (640, 480)
FRAME_RATE: int = 30


def main() -> None:
    pygame.init()
    clock: Clock = Clock()

    screen: Surface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("The REG Game")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        time_passed: int = clock.tick(FRAME_RATE)

        pygame.display.update()


if __name__ == "__main__":
    main()
