from abc import ABC, abstractmethod
from typing import Any


class BaseView(ABC):
    """
    Abstract base class for all views of the Snake game.
    Defines the common interface that all views must implement.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the view.
        This method is called once at startup.
        """
        pass

    @abstractmethod
    def render(self, game_state: Any, current_strategy: str, speed: int) -> None:
        """
        Display the current game state.

        :param game_state: The game state to display.
        :param current_strategy: The name of the currently active strategy.
        :param speed: The current speed of the game.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Clean up the view resources.
        This method is called at the end of the game.
        """
        pass

    @abstractmethod
    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        :param message: The message to display.
        """
        pass

