import random
import time

import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from framework import Game, GameState
from interstitial import InterstitialState
from pygame.surface import Surface
from spritesheet import SpriteSheet

BOARD_SIZE = 6
if BOARD_SIZE < 3:
    raise ValueError("Board size must be at least 3x3 for a playable game.")
PIPE_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // BOARD_SIZE  # Size of each pipe square
MARGIN_X = (SCREEN_WIDTH - BOARD_SIZE * PIPE_SIZE) // 2
MARGIN_Y = (SCREEN_HEIGHT - BOARD_SIZE * PIPE_SIZE) // 2

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 150, 0)
random.seed(42)  # For reproducibility in random path generation


class Pipe:
    """Represents a single pipe segment on the board."""

    def __init__(
        self,
        type: str,
        rotation: int = 0,
        colour: tuple[int, int, int] = GRAY,
        draw_manual: bool = True,
        pipe_image_sheet: str = "img/icon1.png",
        pipe_image_green_sheet: str = "img/icon1_success.png",
    ):
        # type can be:
        # 'straight': | or -
        # 'corner': L-shaped
        # 't_joint': T-shaped
        # 'start_end': special type for start and end points
        # 'empty': represents an impassable cell with no connections
        self.type = type

        # rotation: 0, 90, 180, 270 degrees (clockwise)
        # Represents the current visual orientation
        self.rotation = rotation

        self.colour = colour

        # draw: whether to draw the pipe segment manually (True) or load it from a spritesheet
        self.draw_manual = draw_manual
        if self.draw_manual:
            # If drawing manually, we don't need the sprite sheet
            self.pipe_image = None
            self.pipe_image_green = None
        else:
            # depending on the colour, use the appropriate row to get the pipe image
            # depending on the type, use the appropriate row and column to get the pipe image
            # depdening on the rotation, use the approriate transform to rotate the image
            image_size = 30
            total_rotation = self.rotation
            if self.type == "straight":
                pipe_image_x = 10
                pipe_image_y = 41
                total_rotation += 90
            elif self.type == "corner":
                pipe_image_x = 74
                pipe_image_y = 41
            elif self.type == "t_joint":
                pipe_image_x = 42
                pipe_image_y = 41
                total_rotation += 90
            elif self.type == "start_end":
                pipe_image_x = 74
                pipe_image_y = 73
            else:
                # also for 'empty' type
                pipe_image_x = 0
                pipe_image_y = 0
                image_size = 6

            # Get the image from the sprite sheet
            self.pipe_image = SpriteSheet(pipe_image_sheet).get_image(
                pipe_image_x, pipe_image_y, image_size, image_size
            )
            self.pipe_image_green = SpriteSheet(pipe_image_green_sheet).get_image(
                pipe_image_x, pipe_image_y, image_size, image_size
            )

            # Rotate the image based on the initial rotation
            if total_rotation != 0:
                self.pipe_image = pygame.transform.rotate(
                    self.pipe_image, -total_rotation
                )
                self.pipe_image_green = pygame.transform.rotate(
                    self.pipe_image_green, -total_rotation
                )

            # Scale the image to fit the pipe size
            self.pipe_image = pygame.transform.scale(
                self.pipe_image, (PIPE_SIZE, PIPE_SIZE)
            )
            self.pipe_image_green = pygame.transform.scale(
                self.pipe_image_green, (PIPE_SIZE, PIPE_SIZE)
            )

        # Define connections for each pipe type in its default (0 degree) rotation.
        # Connections are represented by a set of directions: 'N', 'E', 'S', 'W'
        # 'N': North (up), 'E': East (right), 'S': South (down), 'W': West (left)
        self.base_connections = self._define_base_connections()

    def _define_base_connections(self):
        """Defines the connections for each pipe type in its default rotation."""
        if self.type == "straight":
            return {"N", "S"}
        elif self.type == "corner":
            return {"N", "E"}
        elif self.type == "t_joint":
            return {"N", "E", "W"}
        elif self.type == "start_end":
            return {"N", "E", "S", "W"}
        elif self.type == "empty":
            return set()
        else:
            return set()

    def get_current_connections(self):
        """Calculates the current connections based on rotation."""
        if self.type == "empty":
            return set()
        if self.type == "start_end":
            if self.rotation == 0:
                return {"N"}
            elif self.rotation == 90:
                return {"E"}
            elif self.rotation == 180:
                return {"S"}
            elif self.rotation == 270:
                return {"W"}

        connections = set()
        directions = ["N", "E", "S", "W"]
        # Map rotation to index shift
        rotation_index_shift = self.rotation // 90

        for conn in self.base_connections:
            try:
                # Find the index of the base connection direction
                idx = directions.index(conn)
                # Apply the rotation shift to get the new index, wrap around if necessary
                new_idx = (idx + rotation_index_shift) % 4
                connections.add(directions[new_idx])
            except ValueError:
                # This should not happen if base_connections are valid directions
                pass

        return connections

    def rotate(self):
        """Rotates the pipe 90 degrees clockwise."""
        # Only rotate if the pipe is not 'empty'
        if self.type != "empty":
            self.rotation = (self.rotation + 90) % 360

        if self.pipe_image:
            self.pipe_image = pygame.transform.rotate(self.pipe_image, -90)

        if self.pipe_image_green:
            self.pipe_image_green = pygame.transform.rotate(self.pipe_image_green, -90)

        print(f"Rotated pipe of type '{self.type}' to {self.rotation} degrees.")

    def draw(self, surface: Surface, x: int, y: int):
        """Draws the pipe segment on the given surface."""
        if self.draw_manual:
            # Add a small border effect
            rect = pygame.Rect(x + 2, y + 2, PIPE_SIZE - 4, PIPE_SIZE - 4)

            # Draw background square
            pygame.draw.rect(surface, self.colour, rect, border_radius=5)

            # Only draw lines if the pipe is not empty
            if self.type != "empty":
                # Draw the pipe lines based on current connections
                center_x = x + PIPE_SIZE // 2
                center_y = y + PIPE_SIZE // 2
                line_thickness = 5

                # Draw lines based on type and rotation
                connections = self.get_current_connections()
                if "N" in connections:
                    pygame.draw.line(
                        surface,
                        BLACK,
                        (center_x, center_y),
                        (center_x, y),
                        line_thickness,
                    )
                if "E" in connections:
                    pygame.draw.line(
                        surface,
                        BLACK,
                        (center_x, center_y),
                        (x + PIPE_SIZE, center_y),
                        line_thickness,
                    )
                if "S" in connections:
                    pygame.draw.line(
                        surface,
                        BLACK,
                        (center_x, center_y),
                        (center_x, y + PIPE_SIZE),
                        line_thickness,
                    )
                if "W" in connections:
                    pygame.draw.line(
                        surface,
                        BLACK,
                        (center_x, center_y),
                        (x, center_y),
                        line_thickness,
                    )

                # Draw a small circle in the center
                pygame.draw.circle(
                    surface, BLACK, (center_x, center_y), line_thickness // 2 + 1
                )
        else:
            # Draw the pipe image on the surface
            if self.colour == GREEN:
                # Use the green pipe image if the pipe is part of the solution path
                surface.blit(self.pipe_image_green, (x, y))
            else:
                surface.blit(self.pipe_image, (x, y))


class Board:
    """Manages the grid of pipes and game logic."""

    def __init__(self, size: int, draw_manual: bool = True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        # Start in top-left corner or adjacent
        self.start_pos = random.choice([(0, 0), (0, 1), (1, 0)])
        # End in bottom-right corner or adjacent up to half way
        self.end_pos = random.choice(
            [(size - 1, col) for col in range((size // 2) + 1, size)]
            + [(row, size - 1) for row in range((size // 2) + 1, size)]
        )
        # Whether to draw the pipe segment manually (True) or load it from a spritesheet
        self.draw_manual = draw_manual
        self._initialize_board()

    def is_valid_move(self, rows: int, cols: int, r: int, c: int, visited: set) -> bool:
        """
        Checks if a cell is within grid boundaries and has not been visited.
        """
        return 0 <= r < rows and 0 <= c < cols and (r, c) not in visited

    def find_random_path(
        self, rows: int, cols: int, start: tuple, end: tuple
    ) -> list[tuple[int, int]] | None:
        """
        Randomly generates a path between start and end points on a grid.
        """
        if not (
            0 <= start[0] < rows
            and 0 <= start[1] < cols
            and 0 <= end[0] < rows
            and 0 <= end[1] < cols
        ):
            print("Start or end point out of bounds.")
            return None

        # Stack for DFS: stores (row, col, current_path_list)
        stack = [(start[0], start[1], [start])]
        visited = set()
        visited.add(start)

        # Possible moves: (dr, dc) for up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            # Pop the current state (last element of stack)
            r, c, current_path = stack.pop()

            # If we reached the end, return the path
            if (r, c) == end:
                return current_path

            # Get valid neighbors and randomize their order
            neighbors = []
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if self.is_valid_move(rows, cols, nr, nc, visited):
                    neighbors.append((nr, nc))

            # Randomize the order of neighbors to ensure varied paths
            random.shuffle(neighbors)

            # Push valid, unvisited neighbors onto the stack
            for nr, nc in neighbors:
                # Mark as visited when pushing to prevent cycles in this path search
                # This ensures that each generated path is simple (no repeated cells).
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc, current_path + [(nr, nc)]))

        raise ValueError("No valid path found from start to end.")

    def _initialize_board(self):
        """Fills the board with a guaranteed solvable path and random other pipes/empty cells."""
        # Only include 'straight' and 'corner' for generation
        pipe_types = ["straight", "corner", "t_joint"]
        empty_cell_probability = 0.25

        # 1. Generate a solvable path (sequence of (r, c) tuples)
        self.solution_path = self.find_random_path(
            self.size, self.size, self.start_pos, self.end_pos
        )

        # 2. Populate self.grid with path pipes in their correct solution orientations
        for i in range(len(self.solution_path)):
            r, c = self.solution_path[i]

            if (r, c) == self.start_pos:
                # start pipe: determine its rotation based on the first move direction
                direction = (
                    self.solution_path[i + 1][0] - r,
                    self.solution_path[i + 1][1] - c,
                )
                if direction == (0, 1):  # Move East from start
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=90,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (1, 0):  # Move South
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=180,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (0, -1):  # Move West
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=270,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (-1, 0):  # Move North
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=0,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
            elif (r, c) == self.end_pos:
                # end pipe: determine its rotation based on the last move direction
                direction = (
                    self.solution_path[i - 1][0] - r,
                    self.solution_path[i - 1][1] - c,
                )
                if direction == (0, 1):  # Move East to end
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=90,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (1, 0):  # Move South to end
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=180,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (0, -1):  # Move West to end
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=270,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
                elif direction == (-1, 0):  # Move North to end
                    self.grid[r][c] = Pipe(
                        type="start_end",
                        rotation=0,
                        colour=RED,
                        draw_manual=self.draw_manual,
                    )
            else:
                # Determine pipe type and rotation for intermediate path segments
                prev_r, prev_c = self.solution_path[i - 1]
                next_r, next_c = self.solution_path[i + 1]

                # Determine incoming and outgoing directions
                incoming_dir = ""
                if prev_r == r - 1:
                    incoming_dir = "N"  # Came from North (prev is above)
                elif prev_r == r + 1:
                    incoming_dir = "S"  # Came from South (prev is below)
                elif prev_c == c - 1:
                    incoming_dir = "W"  # Came from West (prev is left)
                elif prev_c == c + 1:
                    incoming_dir = "E"  # Came from East (prev is right)

                outgoing_dir = ""
                if next_r == r - 1:
                    outgoing_dir = "N"  # Going North (next is above)
                elif next_r == r + 1:
                    outgoing_dir = "S"  # Going South (next is below)
                elif next_c == c - 1:
                    outgoing_dir = "W"  # Going West (next is left)
                elif next_c == c + 1:
                    outgoing_dir = "E"  # Going East (next is right)

                # Assign pipe based on incoming and outgoing directions
                pipe_type, rotation = self._get_pipe_type_and_rotation(
                    incoming_dir, outgoing_dir
                )
                self.grid[r][c] = Pipe(
                    type=pipe_type,
                    rotation=rotation,
                    draw_manual=self.draw_manual,
                )

        # 3. Fill the rest of the board with random pipes or empty cells
        path_visited = set(self.solution_path)
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in path_visited:
                    if random.random() < empty_cell_probability:
                        self.grid[r][c] = Pipe(
                            "empty",
                            rotation=0,
                            draw_manual=self.draw_manual,
                        )
                    else:
                        self.grid[r][c] = Pipe(
                            type=random.choice(pipe_types),
                            rotation=random.choice([0, 90, 180, 270]),
                            draw_manual=self.draw_manual,
                        )

        self.check_connections()  # Initial check to set up colours

    def _get_pipe_type_and_rotation(self, dir1: str, dir2: str) -> tuple[str, int]:
        """Helper to determine pipe type and rotation for a segment of the path."""
        dirs = tuple(sorted([dir1, dir2]))

        # with probability 0.2 return a t-joint pipe which is valid for
        # cases where corner or straight pipes are neededd
        if random.random() < 0.2:
            return ("t_joint", random.choice([0, 90, 180, 270]))

        if dirs in {("N", "S"), ("E", "W"), ("S", "N"), ("W", "E")}:
            # straight pipe
            return ("straight", random.choice([0, 90, 180, 270]))

        if dirs in {
            ("N", "E"),
            ("N", "W"),
            ("E", "N"),
            ("E", "S"),
            ("W", "N"),
            ("W", "S"),
            ("S", "E"),
            ("S", "W"),
        }:
            # corner pipe
            return ("corner", random.choice([0, 90, 180, 270]))

        # This fallback shouldn't be hit with a valid path
        print(
            f"Warning: Unexpected directions for path pipe: {dir1}, {dir2}. Defaulting to t_joint."
        )
        return ("t_joint", random.choice([0, 90]))

    def get_pipe_at_coords(
        self, mouse_x: int, mouse_y: int
    ) -> tuple[Pipe | None, int | None, int | None]:
        """Converts screen coordinates to grid coordinates and returns the pipe."""
        col = (mouse_x - MARGIN_X) // PIPE_SIZE
        row = (mouse_y - MARGIN_Y) // PIPE_SIZE
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col], row, col

        return None, None, None

    def rotate_pipe(self, row: int, col: int) -> bool:
        """Rotates the pipe at the given grid coordinates."""
        # Only allow rotation if it's not a start/end point AND not an empty pipe
        current_pipe = self.grid[row][col]
        if current_pipe is None:
            return False

        if (row, col) not in {
            self.start_pos,
            self.end_pos,
        } and current_pipe.type != "empty":
            current_pipe.rotate()
            # After rotation, re-check connections and update colours
            return self.check_connections()

        # Return False if rotation is not allowed or pipe is empty
        return False

    def check_connections(self):
        """
        Performs a Breadth-First Search (BFS) from the start pipe
        to find all connected pipes and update their colours.
        """
        # Reset colours for all pipes before checking connections
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) == self.start_pos or (r, c) == self.end_pos:
                    self.grid[r][c].colour = RED  # Start/end points are initially red
                elif self.grid[r][c].type == "empty":
                    self.grid[r][c].colour = BLACK  # Empty cells are black
                else:
                    self.grid[r][c].colour = GRAY  # All other pipes revert to gray

        q = [(self.start_pos[0], self.start_pos[1])]
        visited = set()
        connected_pipes = set()

        # Add the start position to the set of connected pipes to begin the BFS
        connected_pipes.add(self.start_pos)

        # BFS algorithm to traverse connected pipes
        while q:
            r, c = q.pop(0)
            if (r, c) in visited:
                continue
            visited.add((r, c))

            current_pipe = self.grid[r][c]
            current_connections = current_pipe.get_current_connections()

            # Define neighbors and the required connection direction from them
            neighbors = {
                "N": (r - 1, c, "S"),
                "E": (r, c + 1, "W"),
                "S": (r + 1, c, "N"),
                "W": (r, c - 1, "E"),
            }

            for direction, (nr, nc, required_neighbor_conn) in neighbors.items():
                if direction in current_connections:
                    # Check if current pipe connects in this direction
                    # Check if neighbor is within board bounds
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        neighbor_pipe = self.grid[nr][nc]
                        # Only consider connecting to non-empty pipes
                        if neighbor_pipe.type != "empty":
                            neighbor_connections = (
                                neighbor_pipe.get_current_connections()
                            )
                            # If neighbor also connects back to current pipe and not yet visited
                            if required_neighbor_conn in neighbor_connections:
                                if (nr, nc) not in visited:
                                    q.append((nr, nc))
                                    # Add to connected_pipes as soon as it's queued
                                    connected_pipes.add((nr, nc))

        # Update colours based on the full set of connected pipes
        # Intermediate pipes in the path turn GREEN
        for r, c in connected_pipes:
            if (r, c) != self.start_pos and (r, c) != self.end_pos:
                self.grid[r][c].colour = GREEN

        # Determine if the end pipe is reached, indicating a win
        is_game_won = self.end_pos in connected_pipes
        if is_game_won:
            # If game is won, colour the start and end points as part of the winning path
            self.grid[self.start_pos[0]][self.start_pos[1]].colour = GREEN
            self.grid[self.end_pos[0]][self.end_pos[1]].colour = GREEN

        return is_game_won

    def draw(self, surface: Surface):
        """Draws all pipes on the board."""
        for r in range(self.size):
            for c in range(self.size):
                pipe = self.grid[r][c]
                if pipe is None:
                    continue

                x = MARGIN_X + c * PIPE_SIZE
                y = MARGIN_Y + r * PIPE_SIZE
                pipe.draw(surface, x, y)

                # Draw thin black grid lines for better visualization
                pygame.draw.rect(surface, BLACK, (x, y, PIPE_SIZE, PIPE_SIZE), 1)

    def draw_hover_highlight(self, surface: Surface, mouse_x: int, mouse_y: int):
        """Draws a highlight rectangle over the pipe currently being hovered."""
        pipe, row, col = self.get_pipe_at_coords(mouse_x, mouse_y)
        # Only highlight if it's not a start/end point and not an empty pipe
        if (
            pipe
            and row is not None
            and col is not None
            and (row, col) not in [self.start_pos, self.end_pos]
            and pipe.type != "empty"
        ):
            x = MARGIN_X + col * PIPE_SIZE
            y = MARGIN_Y + row * PIPE_SIZE
            pygame.draw.rect(
                surface, YELLOW, (x, y, PIPE_SIZE, PIPE_SIZE), 3, border_radius=5
            )


class PipeGameState(GameState):
    def __init__(
        self,
        game: Game,
        game_over_state: GameState | None = None,
        play_game_state: GameState | None = None,
        board_size: int = 6,
        draw_manual: bool = False,
    ):
        if board_size < 3:
            raise ValueError("Board size must be at least 3x3 for a playable game.")
        super().__init__(game)
        self.game_over_state = game_over_state
        self.play_game_state = play_game_state
        self.board_size = board_size
        self.draw_manual = draw_manual

    def on_enter(self, previous_state: GameState | None):
        self.board = Board(self.board_size, self.draw_manual)
        self.game_won = False

    def on_exit(self):
        self.board = None
        self.game_won = False

    def update(self, game_time: int, pos: tuple[int, int] | None, *args, **kwargs):
        if pos is None:
            return

        # Extract mouse position from the provided tuple
        mouse_x, mouse_y = pos
        pipe, row, col = self.board.get_pipe_at_coords(mouse_x, mouse_y)

        # Only allow pipe rotation if a pipe was clicked and the game hasn't been won
        # and the clicked pipe is not an empty cell
        # Rotate_pipe updates colours and returns win status
        if pipe and row is not None and col is not None and not self.game_won:
            self.game_won = self.board.rotate_pipe(row, col)

    def draw(self, surface: Surface):
        surface.fill(WHITE)
        self.board.draw(surface)

        # Draw hover highlight if the game is not won
        if not self.game_won:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.board.draw_hover_highlight(surface, mouse_x, mouse_y)

        pygame.display.flip()

        # Display text if the game is won
        if self.game_won:
            time.sleep(2)
            self.end_game()

    def end_game(self):
        if self.play_game_state is not None:
            # change state of the machine (to inactive)
            for terminal in self.play_game_state.terminal_controller.terminals:
                if terminal.state_machine.active_state.name == "fixing":
                    terminal.state_machine.set_state("unhackable")

            # change the state of the hackers to wandering (random)
            for hacker in self.play_game_state.maisy_controller.hacker_models:
                if hacker.brain.active_state.name == "fighting":
                    hacker.brain.set_state("wandering")

            get_ready_state: InterstitialState = InterstitialState(
                self.game, "Hacker stopped!", 4500, self.play_game_state
            )
            self.game.change_state(get_ready_state)
            return

        game_over_state: InterstitialState = InterstitialState(
            self.game, "You won!", 4500, self.game_over_state
        )
        self.game.change_state(game_over_state)
        return
