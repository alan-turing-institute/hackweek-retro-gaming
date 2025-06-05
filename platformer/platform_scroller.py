import pygame
import constants
from pygame.surface import Surface
from pygame.sprite import Group
from platplayer import Player
from levels import Level, FirstLevel, SecondLevel
from pygame.time import Clock


def main() -> None:
    pygame.init()

    size: tuple[int, int] = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    screen: Surface = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer")

    player: Player = Player()
    level_list: list[Level] = []
    level_list.append(FirstLevel(player))
    level_list.append(SecondLevel(player))

    current_level_index: int = 0
    current_level: Level = level_list[current_level_index]

    active_sprite_list: Group = Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done: bool = False
    clock: Clock = Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()
        current_level.update()

        if player.rect.right >= 500:
            difference: int = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-difference)

        if player.rect.left <= 120:
            difference = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(difference)

        current_position: int = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_index < len(level_list) - 1:
                current_level_index += 1
                current_level = level_list[current_level_index]
                player.level = current_level

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
