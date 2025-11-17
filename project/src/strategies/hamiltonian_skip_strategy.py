from .movement_strategy import MovementStrategy
import random


class HamiltonianSkipMovementStrategy(MovementStrategy):
    """
    A strategy that follows a pre-calculated Hamiltonian cycle.
    This allows the snake to fill the entire grid without collisions.
    """

    def __init__(self, grid_width: int, grid_height: int, random_cycle: bool):
        """
        Initialize the strategy and generate the Hamiltonian cycle.

        :param grid_width: The width of the game grid.
        :param grid_height: The height of the game grid.
        :param random_cycle: Whether to generate a random cycle.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.hamiltonian_cycle: list[tuple[int, int]] = []
        if random_cycle:
            self._generate_random_hamiltonian_cycle()
        else:
            self._generate_hamiltonian_cycle()

    def _generate_hamiltonian_cycle(self) -> None:
        """
        Generate a Hamiltonian cycle for the given grid dimensions.
        """
        cycle: list[tuple[int, int]] = []
        visited: set[tuple[int, int]] = set()

        current_pos = (0, 0)
        ws = self.grid_width - 1  # world size - 1
        max_y = self.grid_height - 1

        while True:
            curr_x, curr_y = current_pos

            if current_pos in visited and current_pos != (0, 0):
                break

            cycle.append(current_pos)
            visited.add(current_pos)

            is_up = (curr_x % 2 == 0)
            # Convert to the original coordinate system (y=0 at the bottom)
            original_y = max_y - curr_y

            next_direction = None

            if is_up and original_y != max_y and (original_y != 0 or curr_x == 0):
                next_direction = (0, -1)  # North (our y decreases)
            elif is_up and original_y == max_y or (not is_up and original_y == 1 and curr_x != ws):
                next_direction = (1, 0)   # East
            elif original_y == 0 and curr_x != 0:
                next_direction = (-1, 0)  # West
            elif original_y != 0 and (original_y > 1 or curr_x == ws):
                next_direction = (0, 1)   # South (our y increases)

            if next_direction is None:
                break

            new_pos_x = curr_x + next_direction[0]
            new_pos_y = curr_y + next_direction[1]

            if new_pos_x < 0 or new_pos_x >= self.grid_width or new_pos_y < 0 or new_pos_y >= self.grid_height:
                break

            new_pos = (new_pos_x, new_pos_y)

            if new_pos == (0, 0) and len(cycle) > 1:
                break

            current_pos = new_pos

        self.hamiltonian_cycle = cycle

    def _generate_random_hamiltonian_cycle(self):
        """
        Generate a hamiltonian cycle for the given grid dimensions.
        1. Create a spanning tree (maze) on a grid of size / 2 via the Prim's algorithm.
        2. Walk along the walls of this maze on the real grid, turning left as soon as possible, to generate the cycle.
        """
        if self.grid_width % 2 != 0 or self.grid_height % 2 != 0:
            # If the dimensions are odd, fall back to the non-random cycle
            return self._generate_hamiltonian_cycle()

        maze_width = self.grid_width // 2
        maze_height = self.grid_height // 2

        # --- 1. Generate the spanning tree of the maze (Prim's algorithm) ---

        # maze_tree stores the maze as an adjacency list
        maze_tree = { (mx, my): set() for mx in range(maze_width) for my in range(maze_height) }
        visited = set()
        # 'walls' is a set of potential walls to break
        # A wall is a tuple of two cells (cell1, cell2)
        walls = set()

        # Start from a random cell of the maze
        start_cell = (random.randrange(maze_width), random.randrange(maze_height))
        visited.add(start_cell)

        # Add the initial walls of the starting cell
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (start_cell[0] + dx, start_cell[1] + dy)
            if 0 <= neighbor[0] < maze_width and 0 <= neighbor[1] < maze_height:
                # 'sorted' avoids duplicates like (A, B) and (B, A)
                walls.add(tuple(sorted((start_cell, neighbor))))

        while walls:
            # Choose a random wall
            wall = random.choice(list(walls))
            walls.remove(wall)
            cell1, cell2 = wall

            # If only one side of the wall has been visited, break the wall
            if (cell1 in visited) != (cell2 in visited):
                # Add a passage in the tree
                maze_tree[cell1].add(cell2)
                maze_tree[cell2].add(cell1)

                # Add the new cell to the maze
                new_cell = cell2 if cell1 in visited else cell1
                visited.add(new_cell)

                # Add the walls of the new cell
                nx, ny = new_cell
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    neighbor = (nx + dx, ny + dy)
                    if 0 <= neighbor[0] < maze_width and 0 <= neighbor[1] < maze_height and neighbor not in visited:
                        walls.add(tuple(sorted((new_cell, neighbor))))

        # --- 2. Walk along the walls of this maze on the real grid, turning left as soon as possible, to generate the cycle. ---

        def is_passage(current_pos: tuple[int, int], move_dir: tuple[int, int]) -> bool:
            """Check if a movement is allowed (passage or intra-cellule)."""
            new_pos = (current_pos[0] + move_dir[0], current_pos[1] + move_dir[1])

            # Check the limits of the complete grid
            if not (0 <= new_pos[0] < self.grid_width and 0 <= new_pos[1] < self.grid_height):
                return False

            # Find the cells of the maze (half-size)
            maze_pos1 = (current_pos[0] // 2, current_pos[1] // 2)
            maze_pos2 = (new_pos[0] // 2, new_pos[1] // 2)

            # Movement allowed if it stays in the same cell of the maze (2x2 block)
            if maze_pos1 == maze_pos2:
                return True

            # Movement allowed if there is a passage in the tree of the maze
            if maze_pos2 in maze_tree[maze_pos1]:
                return True

            # Otherwise, it's a solid wall
            return False

        cycle = []
        pos = (0, 0)
        # Start looking towards the East
        direction = (1, 0)  # (dx, dy)

        for _ in range(self.grid_width * self.grid_height):
            cycle.append(pos)

            # Determine the relative directions
            left_dir = (-direction[1], direction[0])
            front_dir = direction
            right_dir = (direction[1], -direction[0])

            # Rule: Turn left if possible, otherwise straight, otherwise right
            if is_passage(pos, left_dir):
                direction = left_dir
            elif is_passage(pos, front_dir):
                direction = front_dir
            else:
                # If left and straight are blocked, right must be open
                direction = right_dir
            
            # Move in the new direction
            pos = (pos[0] + direction[0], pos[1] + direction[1])

        self.hamiltonian_cycle = cycle

    def get_neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int, int]]:
        """
        Get the neighbors of a given position.
        """
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if 0 <= new_pos[0] < self.grid_width and 0 <= new_pos[1] < self.grid_height:
                neighbors.append(
                    (new_pos, self.hamiltonian_cycle.index(new_pos)))
        return neighbors

    def get_distance(self, ham_index1: int, ham_index2: int) -> int:
        """
        Get the distance between two Hamiltonian indices.
        """
        # If the length of the cycle if 16 the max index is 15 so dist(15, 0) = 1 because we loop around
        # dist(0, 15) = 15
        # dist(1, 15) = 14
        # ...

        if ham_index1 < ham_index2:
            return ham_index2 - ham_index1
        else:
            return (len(self.hamiltonian_cycle) - ham_index1 + ham_index2) % len(self.hamiltonian_cycle)

    def get_move(self, snake_body: list[tuple[int, int]], food_pos: tuple[int, int] | None) -> tuple[int, int]:
        """
        Determine the next movement following the Hamiltonian cycle.

        :param snake_body: The current body of the snake.
        :param food_pos: (Not used by this strategy).
        :return: The (dx, dy) direction towards the next cell in the cycle.
        """
        if not self.hamiltonian_cycle:
            return (1, 0)  # Default movement if the cycle generation failed

        head = snake_body[0]
        tail = snake_body[-1]
        apple = food_pos
        try:
            head_ham_index = self.hamiltonian_cycle.index(head)
            tail_ham_index = self.hamiltonian_cycle.index(tail)
            apple_ham_index = self.hamiltonian_cycle.index(apple)
        except ValueError:
            # The snake head is not on the cycle (e.g., after a reset).
            # Return a default movement.
            return (1, 0)

        head_neighbors = self.get_neighbors(head)

        next_cell = None
        snake_percent = len(snake_body) / (self.grid_width * self.grid_height)
        threshold = 0.5
        if head_ham_index > tail_ham_index and snake_percent < threshold:
            # remove neighbors with index between tail_ham_index and head_ham_index
            head_neighbors = [neighbor for neighbor in head_neighbors if neighbor[1]
                              < tail_ham_index or neighbor[1] > head_ham_index]
            # Sort neighbors by distance to apple
            head_neighbors.sort(
                key=lambda x: self.get_distance(x[1], apple_ham_index))
            # For each neighbor if the distance with the tail is less than 10% of free space, remove it
            free_space = 5
            head_neighbors = [
                neighbor for neighbor in head_neighbors if self.get_distance(neighbor[1], tail_ham_index) > free_space
            ]
            if head_neighbors:
                next_cell = head_neighbors[0][0]
        elif head_ham_index < tail_ham_index and snake_percent < threshold:
            # keep neighbors with index between head_ham_index and tail_ham_index
            head_neighbors = [neighbor for neighbor in head_neighbors if neighbor[1]
                              > head_ham_index and neighbor[1] < tail_ham_index]
            # Sort neighbors by distance to apple
            head_neighbors.sort(
                key=lambda x: self.get_distance(x[1], apple_ham_index))
            # For each neighbor if the distance with the tail is less than 10% of free space, remove it
            free_space = 5
            head_neighbors = [
                neighbor for neighbor in head_neighbors if self.get_distance(neighbor[1], tail_ham_index) > free_space
            ]
            if head_neighbors:
                next_cell = head_neighbors[0][0]
        elif head_ham_index == tail_ham_index:
            # Shortest path to the apple
            head_neighbors.sort(
                key=lambda x: self.get_distance(x[1], apple_ham_index))
            if head_neighbors:
                next_cell = head_neighbors[0][0]

        if next_cell is None:
            next_index = (head_ham_index + 1) % len(self.hamiltonian_cycle)
            next_cell = self.hamiltonian_cycle[next_index]

        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]

        # Normalize (should be only -1, 0, or 1, but it's a good practice)
        if dx != 0:
            dx = 1 if dx > 0 else -1
        if dy != 0:
            dy = 1 if dy > 0 else -1

        return (dx, dy)
