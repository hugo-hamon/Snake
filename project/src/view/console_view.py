from ..model.game_state import GameState
from .base_view import BaseView
import platform
import os
import sys


class ConsoleView(BaseView):
    """
    Console view that displays the Snake game in the terminal.
    Uses ASCII characters to represent the snake and food.
    """

    def __init__(self, config: dict):
        """
        Initialize the console view.

        :param config: Game configuration.
        """
        self.config = config

        self.grid_width = config["game"]["grid_width"]
        self.grid_height = config["game"]["grid_height"]
        self.first_render = True

    def initialize(self) -> None:
        """Initialize the console view."""
        self.clear_screen()
        print("=== SNAKE GAME - CONSOLE VIEW ===")
        print()

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def move_cursor_to_top(self) -> None:
        """Move cursor to the top of the terminal without clearing."""
        if platform.system() != "Windows":
            # ANSI escape code to move cursor to home position
            sys.stdout.write("\033[H")
            sys.stdout.flush()
        else:
            # For Windows, we can try to use ANSI codes if supported
            try:
                sys.stdout.write("\033[H")
                sys.stdout.flush()
            except:
                # Fallback: clear screen on Windows if ANSI not supported
                os.system('cls')

    def render(self, game_state: GameState, current_strategy: str, speed: int) -> None:
        """
        Display the current game state in the terminal.

        :param game_state: The game state to display.
        :param current_strategy: The name of the currently active strategy.
        :param speed: The current speed of the game.
        """
        # On first render, clear screen. After that, just move cursor to top
        if self.first_render:
            self.clear_screen()
            self.first_render = False
        else:
            self.move_cursor_to_top()
        
        # Calculate the width for proper alignment
        # Each cell takes 2 characters ("◉ "), so grid takes grid_width * 2 chars
        # Plus 2 spaces for padding (one on each side after ║)
        inner_width = self.grid_width * 2 + 2
        border_line = "═" * inner_width
        
        # Header
        print("╔" + border_line + "╗")
        
        # Score line with proper padding
        score_text = f" SNAKE - Score: {game_state.score} "
        padding_needed = inner_width - len(score_text)
        score_line = "║" + score_text + " " * padding_needed + "║"
        print(score_line)
        
        print("╠" + border_line + "╣")
        
        # Game grid
        for y in range(self.grid_height):
            row = "║ "
            for x in range(self.grid_width):
                pos = (x, y)
                if pos == game_state.snake.get_head():
                    row += "◉ "  # Snake head
                elif pos in game_state.snake.body:
                    row += "○ "  # Snake body
                elif pos == game_state.food:
                    row += "★ "  # Food
                else:
                    row += "· "  # Empty cell
            row += " ║"
            print(row)
        
        # Footer
        print("╚" + border_line + "╝")
        print()
        
        # Info lines - fixed width to avoid flickering
        info_width = len(border_line) + 2  # +2 for the ║ borders
        
        mode_line = f"Mode: {current_strategy}"
        print(mode_line.ljust(info_width))
        
        teleport_line = f"Teleportation: {'ON' if game_state.wrap_around else 'OFF'}"
        print(teleport_line.ljust(info_width))
        
        speed_line = f"Speed: {speed}ms"
        print(speed_line.ljust(info_width))
        print()
        
        # Game over display
        if game_state.game_over:
            if game_state.win:
                victory_line = "🎉 VICTORY ! 🎉"
                print(victory_line.center(info_width))
            else:
                gameover_line = "💀 GAME OVER ! 💀"
                print(gameover_line.center(info_width))
            
            score_line = f"Final score: {game_state.score}"
            print(score_line.center(info_width))
            print()
            restart_line = "Press SPACE to restart"
            print(restart_line.center(info_width))
        else:
            commands_line = "Commands: WASD/Arrows = Move | 0 = Auto | 1 = Dummy | T = Teleportation | ESC = Quit"
            print(commands_line.ljust(info_width))
        
        # Add some blank lines to clear any leftover text from previous renders
        print("\n" * 3)
        sys.stdout.flush()

    def cleanup(self) -> None:
        """Clean up the console view resources."""
        self.clear_screen()
        print("Thank you for playing!")

    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        :param message: The message to display.
        """
        print(f"\n>>> {message}\n")

