from .movement_strategy import MovementStrategy


class HamiltonianMovementStrategy(MovementStrategy):
    """
    A strategy that follows a pre-calculated Hamiltonian cycle.
    This allows the snake to fill the entire grid without collisions.
    """

    def __init__(self, grid_width: int, grid_height: int):
        """
        Initialize the strategy and generate the Hamiltonian cycle.

        :param grid_width: The width of the game grid.
        :param grid_height: The height of the game grid.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.hamiltonian_cycle: list[tuple[int, int]] = []
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
            elif not is_up and original_y != 0 and (original_y > 1 or curr_x == ws):
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
        try:
            current_index = self.hamiltonian_cycle.index(head)
        except ValueError:
            # The snake head is not on the cycle (e.g., after a reset).
            # Return a default movement.
            return (1, 0)

        next_index = (current_index + 1) % len(self.hamiltonian_cycle)
        next_cell = self.hamiltonian_cycle[next_index]

        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]

        # Normalize (should be only -1, 0, or 1, but it's a good practice)
        if dx != 0:
            dx = 1 if dx > 0 else -1
        if dy != 0:
            dy = 1 if dy > 0 else -1

        return (dx, dy)
