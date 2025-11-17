import time
import sys

import pygame

from ..strategies import PlayerMovementStrategy, HamiltonianMovementStrategy, DummyMovementStrategy, HamiltonianSkipMovementStrategy
from .input_handler import ConsoleInputHandler
from ..view.pygame_view import PygameView
from ..model.game_state import GameState
from ..view.base_view import BaseView


class GameController:
    """
    Main controller that manages the interaction between the model and the view.
    Manages the game loop, user events and coordinates the updates.
    """

    def __init__(self, config: dict, view: BaseView):
        """
        Initialize the game controller.

        :param config: Game configuration.
        :param view: The view to use for display.
        """
        self.config = config
        self.view = view

        # Initialize the game state
        game_config = config["game"]
        self.game_state = GameState(
            grid_width=game_config["grid_width"],
            grid_height=game_config["grid_height"],
            wrap_around=game_config["wrap_around"]
        )

        # Speed configuration
        game_props = config["game"]["properties"]
        self.initial_speed = game_props["initial_speed"]
        self.speed_acceleration = game_props["speed_acceleration"]
        self.min_speed = game_props["min_speed"]
        self.speed = self.initial_speed

        # Movement strategies
        self.player_strategy = PlayerMovementStrategy()
        self.auto_strategy = HamiltonianMovementStrategy(
            game_config["grid_width"],
            game_config["grid_height"],
            config["hamiltonian"]["random_cycle"]
        )
        self.dummy_strategy = DummyMovementStrategy()
        self.hamiltonian_skip_strategy = HamiltonianSkipMovementStrategy(
            game_config["grid_width"],
            game_config["grid_height"],
            config["hamiltonian"]["random_cycle"]
        )

        # Set initial strategy
        if game_config["strategy"].lower() == "cycle":
            self.current_strategy = self.auto_strategy
            self.current_strategy_name = "Cycle"
        elif game_config["strategy"].lower() == "hamiltonian_skip":
            self.current_strategy = self.hamiltonian_skip_strategy
            self.current_strategy_name = "Hamiltonian Skip"
        elif game_config["strategy"].lower() == "player":
            self.current_strategy = self.player_strategy
            self.current_strategy_name = "Player"
        elif game_config["strategy"].lower() == "dummy":
            self.current_strategy = self.dummy_strategy
            self.current_strategy_name = "Dummy"
        else:
            raise ValueError(f"Invalid strategy: {game_config['strategy']}")

        # Game loop state
        self.running = True
        self.last_update_time = 0

        # Handle the timer differently depending on the view
        self.use_pygame_timer = isinstance(self.view, PygameView)
        if self.use_pygame_timer:
            pygame.init()
            self.GAME_UPDATE = pygame.USEREVENT + 1
            pygame.time.set_timer(self.GAME_UPDATE, self.speed)
        else:
            # Console mode: setup input handler
            self.input_handler = ConsoleInputHandler()
            self.input_handler.setup_terminal()

    def reset(self) -> None:
        """Reset the game."""
        self.game_state.reset()
        self.speed = self.initial_speed

        # Reset the strategies
        self.player_strategy = PlayerMovementStrategy((1, 0))
        self.dummy_strategy = DummyMovementStrategy()

        # Keep the current strategy but reset it
        if isinstance(self.current_strategy, PlayerMovementStrategy):
            self.current_strategy = self.player_strategy
        elif isinstance(self.current_strategy, DummyMovementStrategy):
            self.current_strategy = self.dummy_strategy

        if self.use_pygame_timer:
            pygame.time.set_timer(self.GAME_UPDATE, self.speed)

    def update(self) -> None:
        """Update the game logic."""
        if self.game_state.game_over:
            return

        # Get the next direction from the strategy
        direction = self.current_strategy.get_move(
            self.game_state.snake.body,
            self.game_state.food
        )

        # Update the game state
        old_score = self.game_state.score
        self.game_state.update(direction)

        # Increase the speed if the score has increased
        if self.game_state.score > old_score:
            self.speed = max(0, max(self.min_speed, self.speed -
                             self.speed_acceleration))
            if self.use_pygame_timer:
                pygame.time.set_timer(self.GAME_UPDATE, self.speed)

    def handle_pygame_events(self) -> bool:
        """
        Handle the Pygame events.

        :return: False if the game should quit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == self.GAME_UPDATE:
                self.update()

            elif event.type == pygame.KEYDOWN:
                if not self.handle_keydown(event.key):
                    return False

        return True

    def handle_console_input(self) -> bool:
        """
        Handle the console input (non-blocking).

        :return: True to continue, False to quit.
        """
        # Get key press (non-blocking)
        key = self.input_handler.get_key()

        if key:
            # Handle quit
            if key == 'escape' or key == '\x1b':
                return False

            # Handle reset
            elif key == ' ':
                if self.game_state.game_over:
                    self.reset()

            # Handle teleportation toggle
            elif key == 't':
                self.game_state.toggle_wrap_around()

            # Handle strategy changes
            elif key == '0':
                if isinstance(self.current_strategy, HamiltonianMovementStrategy):
                    self.current_strategy = self.player_strategy
                    self.current_strategy_name = "Player"
                else:
                    self.current_strategy = self.auto_strategy
                    self.current_strategy_name = "Auto (H)"

            elif key == '1':
                if isinstance(self.current_strategy, DummyMovementStrategy):
                    self.current_strategy = self.player_strategy
                    self.current_strategy_name = "Player"
                else:
                    self.current_strategy = self.dummy_strategy
                    self.current_strategy_name = "Dummy (D)"

            elif key == '+':
                self.speed += self.speed_acceleration
            elif key == '-':
                self.speed = max(0, self.speed - self.speed_acceleration)
                self.min_speed = max(0, self.min_speed - self.speed_acceleration)

            # Handle player movement (only if in player mode)
            if isinstance(self.current_strategy, PlayerMovementStrategy):
                if key in ('UP', 'w', 'z'):  # Up (z for AZERTY keyboards)
                    self.current_strategy.set_pending_direction(
                        (0, -1), len(self.game_state.snake))
                elif key in ('DOWN', 's'):  # Down
                    self.current_strategy.set_pending_direction(
                        (0, 1), len(self.game_state.snake))
                elif key in ('LEFT', 'a', 'q'):  # Left (q for AZERTY)
                    self.current_strategy.set_pending_direction(
                        (-1, 0), len(self.game_state.snake))
                elif key in ('RIGHT', 'd'):  # Right
                    self.current_strategy.set_pending_direction(
                        (1, 0), len(self.game_state.snake))

        # Update game at regular intervals
        current_time = time.time() * 1000  # Convert to milliseconds

        if current_time - self.last_update_time >= self.speed:
            self.update()
            self.last_update_time = current_time

        return True

    def handle_keydown(self, key: int) -> bool:
        """
        Handle the keydown events.

        :param key: The key code.
        :return: False if the game should quit, True otherwise.
        """
        # Escape to quit
        if key == pygame.K_ESCAPE:
            return False

        # Space to restart
        elif key == pygame.K_SPACE:
            if self.game_state.game_over:
                self.reset()

        # T to toggle the teleportation
        elif key == pygame.K_t:
            self.game_state.toggle_wrap_around()

        # H for the auto mode (Hamiltonian)
        elif key == pygame.K_h:
            if isinstance(self.current_strategy, HamiltonianMovementStrategy):
                self.current_strategy = self.player_strategy
                self.current_strategy_name = "Player"
            else:
                self.current_strategy = self.auto_strategy
                self.current_strategy_name = "Auto (H)"

        # D for the dummy mode
        elif key == pygame.K_d:
            if isinstance(self.current_strategy, DummyMovementStrategy):
                self.current_strategy = self.player_strategy
                self.current_strategy_name = "Player"
            else:
                self.current_strategy = self.dummy_strategy
                self.current_strategy_name = "Dummy (D)"

        # Player controls (only if in player mode)
        if isinstance(self.current_strategy, PlayerMovementStrategy):
            if key == pygame.K_UP or key == pygame.K_w:
                self.current_strategy.set_pending_direction(
                    (0, -1), len(self.game_state.snake))
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.current_strategy.set_pending_direction(
                    (0, 1), len(self.game_state.snake))
            elif key == pygame.K_LEFT or key == pygame.K_a:
                self.current_strategy.set_pending_direction(
                    (-1, 0), len(self.game_state.snake))
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                self.current_strategy.set_pending_direction(
                    (1, 0), len(self.game_state.snake))

        return True

    def run(self) -> None:
        """Start the main game loop."""
        self.view.initialize()

        try:
            while self.running:
                # Handle the events depending on the view type
                if self.use_pygame_timer:
                    self.running = self.handle_pygame_events()
                else:
                    self.running = self.handle_console_input()
                    time.sleep(0.01)  # Small delay to not overload the CPU

                # Display the game state
                self.view.render(
                    self.game_state, self.current_strategy_name, self.speed)

                # Limit the FPS for pygame
                if isinstance(self.view, PygameView):
                    self.view.tick(60)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        finally:
            # Cleanup
            if not self.use_pygame_timer:
                self.input_handler.restore_terminal()

            self.view.cleanup()
            if self.use_pygame_timer:
                pygame.quit()
            sys.exit()
