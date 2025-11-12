from abc import ABC, abstractmethod


class MovementStrategy(ABC):
    """
    Abstract base class for defining snake movement strategies.
    """

    @abstractmethod
    def get_move(self, snake_body: list[tuple[int, int]], food_pos: tuple[int, int] | None) -> tuple[int, int]:
        """
        Compute the next direction for the snake.

        :param snake_body: A list of (x, y) tuples representing the snake's body,
                          where snake_body[0] is the head.
        :param food_pos: A (x, y) tuple for the food's position, or None if there is no food.
        :return: A (dx, dy) tuple representing the next direction (e.g., (1, 0) for right).
        """
        pass

