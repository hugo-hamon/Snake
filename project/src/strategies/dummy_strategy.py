from .movement_strategy import MovementStrategy


class DummyMovementStrategy(MovementStrategy):
    """
    A "dummy" simple strategy that moves naively towards the food.
    It doesn't avoid collisions.
    """

    def __init__(self):
        self.last_move = (1, 0)

    def get_move(self, snake_body: list[tuple[int, int]], food_pos: tuple[int, int] | None) -> tuple[int, int]:
        """
        Move towards the food on one axis at a time.
        Prefer the movement on the X axis, then on the Y axis.
        Avoid making a half-turn.

        :param snake_body: The current body of the snake.
        :param food_pos: The position of the food.
        :return: The (dx, dy) direction.
        """
        if food_pos is None:
            return self.last_move  # No food, continue

        head = snake_body[0]
        head_x, head_y = head
        food_x, food_y = food_pos

        move = (0, 0)

        # Try to move on the X axis first
        if head_x < food_x:
            move = (1, 0)
        elif head_x > food_x:
            move = (-1, 0)
        # If aligned on X, move on the Y axis
        elif head_y < food_y:
            move = (0, 1)
        elif head_y > food_y:
            move = (0, -1)

        # Avoid making a half-turn
        opposite_last_move = (-self.last_move[0], -self.last_move[1])
        if move == opposite_last_move and len(snake_body) > 1:
            # If we try to make a half-turn, try the Y axis instead
            if head_y < food_y:
                move = (0, 1)
            elif head_y > food_y:
                move = (0, -1)
            # If still stuck, use the last move
            elif move == opposite_last_move:
                move = self.last_move

        # Protection if the movement is (0,0) (e.g., on the food)
        if move == (0, 0):
            move = self.last_move

        self.last_move = move
        return self.last_move

