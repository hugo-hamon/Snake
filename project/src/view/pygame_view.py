from ..model.game_state import GameState
from .base_view import BaseView
import pygame

MIN_WINDOW_SIZE = 600

class PygameView(BaseView):
    """
    Pygame view that displays the Snake game with a graphical interface.
    """

    def __init__(self, config: dict):
        """
        Initialize the Pygame view.

        :param config: Game configuration.
        """
        self.config = config
        
        # Grid configuration
        self.grid_width = config["game"]["grid_width"]
        self.grid_height = config["game"]["grid_height"]
        
        # Graphical configuration
        graphics = config["graphics"]
        self.cell_size = graphics["sizes"]["cell_size"]
        self.margin = graphics["sizes"]["margin"]
        
        # Colors
        colors = graphics["colors"]
        self.background_color = tuple(colors["background_color"])
        self.snake_color = tuple(colors["snake_color"])
        self.head_color = tuple(colors["head_color"])
        self.food_color = tuple(colors["food_color"])
        self.text_color = tuple(colors["text_color"])
        self.grid_border_color = tuple(colors["grid_border_color"])
        
        # Font
        font_config = graphics["font"]
        self.font_name = font_config["font_name"]
        self.font_size = font_config["font_size"]
        self.font_size_large = font_config["font_size_large"]
        
        # Compute the window dimensions
        window_width_calc = self.grid_width * self.cell_size + self.margin * 2
        window_height_calc = self.grid_height * self.cell_size + self.margin * 2 + 70
        
        self.window_width = max(window_width_calc, MIN_WINDOW_SIZE)
        self.window_height = max(window_height_calc, MIN_WINDOW_SIZE)
        
        # Pygame variables
        self.screen = None
        self.clock = None
        self.font = None
        self.font_large = None

    def initialize(self) -> None:
        """Initialize Pygame and create the window."""
        pygame.init()
        pygame.display.set_caption("Snake 2D")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.font_large = pygame.font.SysFont(self.font_name, self.font_size_large)

    def get_grid_offset(self) -> tuple[int, int, int]:
        """
        Compute the offsets to center the grid in the window.

        :return: (margin_x, margin_y, bottom_text_y)
        """
        grid_width_px = self.grid_width * self.cell_size
        grid_height_px = self.grid_height * self.cell_size

        top_space = 40
        bottom_space = 80  # Space for 2-3 lines of text

        margin_x = max(self.margin, (self.window_width - grid_width_px) // 2)

        available_height = self.window_height - top_space - bottom_space

        if grid_height_px > available_height:
            margin_y = top_space
            bottom_text_y = margin_y + grid_height_px + 10
        else:
            margin_y = top_space + max(0, (available_height - grid_height_px) // 2)
            bottom_text_y = self.window_height - bottom_space

        return (margin_x, margin_y, bottom_text_y)

    def draw_cell(self, x: int, y: int, color: tuple[int, int, int], margin_x: int, margin_y: int) -> None:
        """
        Draw a cell on the screen.
        
        :param x: x coordinate of the cell.
        :param y: y coordinate of the cell.
        :param color: Color of the cell.
        :param margin_x: Horizontal margin.
        :param margin_y: Vertical margin.
        """
        screen_x = margin_x + x * self.cell_size
        screen_y = margin_y + y * self.cell_size
        rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def draw_text(self, text: str, font: pygame.font.Font, color: tuple, center: tuple[int, int]) -> None:
        """
        Help to draw centered text.
        
        :param text: The text to draw.
        :param font: The font to use.
        :param color: The color of the text.
        :param center: The center position of the text.
        """
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center)
        self.screen.blit(text_surf, text_rect)

    def render(self, game_state: GameState, current_strategy: str, speed: int) -> None:
        """
        Display the current game state.

        :param game_state: The game state to display.
        :param current_strategy: The name of the currently active strategy.
        :param speed: The current speed of the game.
        """
        self.screen.fill(self.background_color)

        margin_x, margin_y, bottom_text_y = self.get_grid_offset()

        # --- Draw the snake ---
        for segment_x, segment_y in game_state.snake.body[1:]:
            self.draw_cell(segment_x, segment_y, self.snake_color, margin_x, margin_y)
        head_x, head_y = game_state.snake.get_head()
        self.draw_cell(head_x, head_y, self.head_color, margin_x, margin_y)

        # --- Draw the food ---
        if game_state.food is not None:
            self.draw_cell(game_state.food[0], game_state.food[1], self.food_color, margin_x, margin_y)

        # --- Draw the UI text ---
        self.draw_text(
            f"Score : {game_state.score}", self.font, self.text_color,
            center=(self.window_width // 2, 20)
        )
        self.draw_text(
            f"Teleportation : {'ON' if game_state.wrap_around else 'OFF'} (T)",
            self.font, self.text_color,
            center=(self.window_width // 2, bottom_text_y)
        )
        self.draw_text(
            f"Mode : {current_strategy}", self.font, self.text_color,
            center=(self.window_width // 2, bottom_text_y + 30)
        )

        # --- Draw the game over / victory screen ---
        if game_state.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            if game_state.win:
                self.draw_text("VICTORY", self.font_large, (50, 255, 50),
                              center=(self.window_width // 2, self.window_height // 2 - 40))
            else:
                self.draw_text("GAME OVER", self.font_large, (255, 50, 50),
                              center=(self.window_width // 2, self.window_height // 2 - 40))

            self.draw_text(f"Final score : {game_state.score}", self.font, self.text_color,
                          center=(self.window_width // 2, self.window_height // 2 + 20))
            self.draw_text("Press SPACE to restart", self.font, self.text_color,
                          center=(self.window_width // 2, self.window_height // 2 + 60))

        # --- Draw the grid border ---
        pygame.draw.rect(
            self.screen,
            self.grid_border_color,
            pygame.Rect(margin_x - 5, margin_y - 5,
                       self.grid_width * self.cell_size + 10,
                       self.grid_height * self.cell_size + 10),
            width=2,
            border_radius=8,
        )

        pygame.display.flip()

    def cleanup(self) -> None:
        """Clean up the Pygame resources."""
        pygame.quit()

    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        :param message: The message to display.
        """
        print(f"[Pygame View] {message}")

    def tick(self, fps: int = 60) -> None:
        """
        Limit the refresh rate.
        
        :param fps: Frames per second.
        """
        if self.clock:
            self.clock.tick(fps)

