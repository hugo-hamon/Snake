from .snake import Snake
import random


class GameState:
    """
    Represents the game state of the Snake game.
    Manages the game logic: the snake, the food, the score, etc.
    """

    def __init__(self, grid_width: int, grid_height: int, wrap_around: bool = True):
        """
        Initialize the game state.

        :param grid_width: Width of the grid.
        :param grid_height: Height of the grid.
        :param wrap_around: If True, the snake teleports to the edges.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.wrap_around = wrap_around
        
        self.snake: Snake | None = None
        self.food: tuple[int, int] | None = None
        self.game_over = False
        self.win = False
        self.score = 0
        
        self.reset()

    def reset(self) -> None:
        """Reset the game to its initial state."""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        
        self.snake = Snake((center_x, center_y), (1, 0))
        self.spawn_food()
        self.game_over = False
        self.win = False
        self.score = 1

    def spawn_food(self) -> None:
        """Spawn the food in a random available cell."""
        all_cells = {(x, y) for x in range(self.grid_width)
                     for y in range(self.grid_height)}
        available = all_cells - set(self.snake.body)
        self.food = random.choice(tuple(available)) if available else None

    def update(self, direction: tuple[int, int]) -> None:
        """
        Update the game logic (a snake movement).
        
        :param direction: The direction (dx, dy) in which to move the snake.
        """
        if self.game_over:
            return

        # 1. Update the direction of the snake
        self.snake.direction = direction

        # 2. Calculate the new position of the head
        head_x, head_y = self.snake.get_head()
        dx, dy = self.snake.direction
        new_head_x = head_x + dx
        new_head_y = head_y + dy

        # 3. Handle the collisions with the walls / teleportation
        if self.wrap_around:
            new_head_x = new_head_x % self.grid_width
            new_head_y = new_head_y % self.grid_height
        elif (new_head_x < 0 or new_head_x >= self.grid_width or
              new_head_y < 0 or new_head_y >= self.grid_height):
            self.end_game()
            return

        new_head = (new_head_x, new_head_y)

        # 4. Check the collision with itself
        if new_head in self.snake.body:
            self.end_game()
            return

        # 5. Check the collision with the food
        if self.food is not None and new_head == self.food:
            self.snake.grow(new_head)
            self.score = len(self.snake)
            self.spawn_food()
        else:
            self.snake.move(new_head)

        # 6. Check the victory
        if len(self.snake) == self.grid_width * self.grid_height:
            self.end_game(win=True)

    def end_game(self, win: bool = False) -> None:
        """
        Stop the game and set the game_over flag.
        
        :param win: If True, the player has won.
        """
        self.game_over = True
        self.win = win

    def toggle_wrap_around(self) -> None:
        """Toggle the teleportation."""
        self.wrap_around = not self.wrap_around

