class Snake:
    """
    Represents the snake in the game.
    Manages its body, movement and growth.
    """

    def __init__(self, start_pos: tuple[int, int], start_direction: tuple[int, int]):
        """
        Initialize the snake.

        :param start_pos: The (x, y) starting position of the snake's head.
        :param start_direction: The (dx, dy) starting direction.
        """
        self.body: list[tuple[int, int]] = [start_pos]
        self.direction = start_direction

    def get_head(self) -> tuple[int, int]:
        """
        :return: The (x, y) coordinates of the snake's head.
        """
        return self.body[0]

    def move(self, new_head: tuple[int, int]) -> None:
        """
        Move the snake to a new head position and remove the tail.

        :param new_head: The (x, y) coordinates of the new head.
        """
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self, new_head: tuple[int, int]) -> None:
        """
        Grow the snake by adding a new head position without removing the tail.

        :param new_head: The (x, y) coordinates of the new head.
        """
        self.body.insert(0, new_head)

    def check_self_collision(self) -> bool:
        """
        Check if the snake's head has collided with its own body.

        :return: True if a collision occurred, False otherwise.
        """
        return self.get_head() in self.body[1:]

    def __len__(self) -> int:
        """
        :return: The length of the snake's body.
        """
        return len(self.body)

    def __contains__(self, item: tuple[int, int]) -> bool:
        """
        Check if a given (x, y) coordinate is part of the snake's body.

        :param item: The (x, y) coordinate to check.
        :return: True if the coordinate is in the snake's body, False otherwise.
        """
        return item in self.body

