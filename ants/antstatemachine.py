import sys
from random import randint

import pygame
from pygame.surface import Surface
from pygame.time import Clock
from vector2 import Vector2

SCREEN_SIZE: tuple[int, int] = (640, 480)
NEST_POSITION: tuple[int, int] = (320, 240)
NEST_SIZE: int = 100
ANT_COUNT: int = 20


class State:
    def __init__(self, name: str):
        self.name: str = name

    def do_actions(self):
        pass

    def check_conditions(self) -> str | None:
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine:
    def __init__(self) -> None:
        self.states: dict[str, State] = {}
        self.active_state: State | None = None

    def add_state(self, state: "State"):
        self.states[state.name] = state

    def think(self) -> None:
        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_name: str | None = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name: str):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class World:
    def __init__(self) -> None:
        self.entities: dict[int, GameEntitity] = {}
        self.entity_id: int = 0

        self.background: Surface = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, NEST_SIZE)

    def add_entity(self, entity: "GameEntitity"):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity: "GameEntitity"):
        del self.entities[entity.id]

    def get(self, entity_id: int | None):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passsed: int) -> None:
        time_passed_seconds: float = time_passsed / 1000.0
        for entity in list(self.entities.values()):
            entity.process(time_passed_seconds)

    def render(self, surface: Surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, e_range=100):
        location_vector: Vector2 = Vector2(*location)

        for entity in self.entities.values():
            if entity.name == name:
                distance = location_vector.get_distance_to(entity.location)
                if distance < e_range:
                    return entity

        return None


class GameEntitity:
    def __init__(self, world: "World", name: str, image: Surface) -> None:
        self.world: "World" = world
        self.name: str = name
        self.image: Surface = image

        self.location: Vector2 = Vector2(0, 0)
        self.destination: Vector2 = Vector2(0, 0)
        self.speed: float = 0.0

        self.brain: StateMachine = StateMachine()

        self.id: int = 0

    def render(self, surface: Surface):
        x, y = self.location
        width, height = self.image.get_size()

        surface.blit(self.image, (x - width / 2, y - height / 2))

    def process(self, time_passed: float) -> None:
        self.brain.think()

        if self.speed > 0 and self.location != self.destination:
            vector_to_destination: Vector2 = self.destination - self.location
            distance_to_destination: float = vector_to_destination.get_length()
            heading: Vector2 = vector_to_destination.get_normalised()
            travel_distance: float = min(
                distance_to_destination, time_passed * self.speed
            )

            self.location += travel_distance * heading


class Leaf(GameEntitity):
    def __init__(self, world: "World", image: Surface):
        super().__init__(world, "leaf", image)


class Spider(GameEntitity):
    def __init__(self, world: "World", image: Surface):
        super().__init__(world, "spider", image)

        self.dead_image: Surface = pygame.transform.flip(image, 0, 1)
        self.health: int = 25
        self.speed: int = 50 + randint(-20, 20)

    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0
            self.image = self.dead_image

        self.speed = 140

    def render(self, surface: Surface):
        super().render(surface)

        x, y = self.location
        width, height = self.image.get_size()

        bar_x: int = x - 12
        bar_y: float = y + height / 2

        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))

    def process(self, time_passed):
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return

        super().process(time_passed)


class AntStateExploring(State):
    def __init__(self, ant: "Ant"):
        super().__init__("exploring")
        self.ant: "Ant" = ant

    def random_destination(self):
        width, height = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, width), randint(0, height))

    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self) -> str | None:
        leaf: GameEntitity | None = self.ant.world.get_close_entity(
            "leaf", self.ant.location
        )

        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"

        spider: GameEntitity | None = self.ant.world.get_close_entity(
            "spider", NEST_POSITION, NEST_SIZE
        )
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100.0:
                self.ant.spider_id = spider.id
                return "hunting"

        return None

    def entry_actions(self):
        self.ant.speed = 120 + randint(-30, 30)
        self.random_destination()


class AntStateSeeking(State):
    def __init__(self, ant: "Ant"):
        super().__init__("seeking")
        self.ant: "Ant" = ant
        self.leaf_id: int | None = None

    def check_conditions(self) -> str | None:
        leaf: GameEntitity | None = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return "exploring"

        if self.ant.location.get_distance_to(leaf.location) < 5:
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
            return "delivering"

        return None

    def entry_actions(self) -> None:
        leaf: GameEntitity | None = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randint(-20, 20)


class AntStateDelivering(State):
    def __init__(self, ant: "Ant"):
        super().__init__("delivering")
        self.ant: "Ant" = ant

    def check_conditions(self) -> str | None:
        if Vector2(NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
            if randint(1, 10) == 1:
                self.ant.drop(self.ant.world.background)
                return "exploring"

        return None

    def entry_actions(self) -> None:
        self.ant.speed = 60.0
        random_offset: Vector2 = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*NEST_POSITION) + random_offset


class AntStateHunting(State):
    def __init__(self, ant: "Ant"):
        super().__init__("hunting")
        self.ant: "Ant" = ant
        self.got_kill: bool = False

    def do_actions(self) -> None:
        spider: Spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return None

        self.ant.destination = spider.location
        if self.ant.location.get_distance_to(spider.location) < 15:
            if randint(1, 5) == 1:
                spider.bitten()

            if spider.health <= 0:
                self.ant.carry(spider.image)
                self.ant.world.remove_entity(spider)
                self.got_kill = True

    def check_conditions(self) -> str | None:
        if self.got_kill:
            return "delivering"

        spider: Spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return "exploring"

        if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 3:
            return "exploring"

        return None

    def entry_actions(self) -> None:
        self.ant.speed = 160 + randint(0, 50)

    def exit_actions(self) -> None:
        self.got_kill = False


class Ant(GameEntitity):
    def __init__(self, world: World, image) -> None:
        super().__init__(world, "ant", image)

        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)

        self.carry_image: Surface | None = None

        self.leaf_id: int | None = None
        self.spider_id: int | None = None

    def carry(self, image: Surface):
        self.carry_image = image

    def drop(self, surface: Surface):
        if self.carry_image:
            x, y = self.location
            width, height = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - width, y - height / 2))
            self.carry_image = None

    def render(self, surface: Surface):
        super().render(surface)

        if self.carry_image:
            x, y = self.location
            width, height = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - width, y - height / 2))


def run() -> None:
    pygame.init()
    screen: Surface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    world: World = World()
    width, height = SCREEN_SIZE

    clock: Clock = Clock()

    ant_image: Surface = pygame.image.load("img/ant.png").convert_alpha()
    leaf_image: Surface = pygame.image.load("img/leaf.png").convert_alpha()
    spider_image: Surface = pygame.image.load("img/spider.png").convert_alpha()

    for ant_number in range(ANT_COUNT):
        ant: Ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, width), randint(0, height))
        ant.brain.set_state("exploring")
        world.add_entity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        time_passed: int = clock.tick(30)

        if randint(1, 10) == 1:
            leaf: Leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, width), randint(0, height))
            world.add_entity(leaf)

        if randint(1, 100) == 1:
            spider: Spider = Spider(world, spider_image)
            spider.location = Vector2(-50, randint(0, height))
            spider.destination = Vector2(width + 50, randint(0, height))
            world.add_entity(spider)

        world.process(time_passed)
        world.render(screen)
        pygame.display.update()


if __name__ == "__main__":
    run()
