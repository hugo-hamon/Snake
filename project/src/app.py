from .view import PygameView, ConsoleView
from .controller import GameController
from .config import load_config


class App:
    def __init__(self, config_path: str) -> None:
        """
        Init the App
        
        :param config_path: Path to the config file
        """
        self.config = load_config(config_path)
        if self.config["game"]["grid_width"] % 2 != 0 or self.config["game"]["grid_height"] % 2 != 0:
            raise ValueError("Grid width and height must be even.")
        
        if self.config["graphics"]["enable"]:
            self.view = PygameView(self.config)
        else:
            self.view = ConsoleView(self.config)
        
        self.controller = GameController(self.config, self.view)

    def run(self) -> None:
        """Run the application."""
        self.controller.run()
