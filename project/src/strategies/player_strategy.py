from .movement_strategy import MovementStrategy


class PlayerMovementStrategy(MovementStrategy):
    """
    A strategy that gets movement commands from the player keyboard.
    """

    def __init__(self, initial_direction: tuple[int, int] = (1, 0)):
        """
        Initialize the player strategy.
        
        :param initial_direction: The starting direction of the snake.
        """
        self.pending_direction = initial_direction
        self.current_direction = initial_direction

    def set_pending_direction(self, new_direction: tuple[int, int], snake_length: int) -> None:
        """
        Set the next direction, preventing the snake from reversing.

        :param new_direction: The desired (dx, dy) from key input.
        :param snake_length: The current length of the snake.
        """
        # Prevent reversing if snake is longer than 1 segment
        if snake_length > 1:
            dx, dy = new_direction
            opposite = (-self.current_direction[0], -self.current_direction[1])
            if (dx, dy) == opposite:
                return
        self.pending_direction = new_direction

    def get_move(self, snake_body: list[tuple[int, int]], food_pos: tuple[int, int] | None) -> tuple[int, int]:
        """
        Return the pending direction set by the player.

        :param snake_body: (Not used by this strategy but required by ABC)
        :param food_pos: (Not used by this strategy but required by ABC)
        :return: The (dx, dy) tuple for the next move.
        """
        self.current_direction = self.pending_direction
        return self.current_direction