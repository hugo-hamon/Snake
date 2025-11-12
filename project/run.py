from src.app import App
import argparse
import logging
import os

LOGGING_CONFIG = {
    "level": logging.INFO,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M:%S",
    "filename": "log/log.log",
    "filemode": "w",
}

DEFAULT_CONFIG_PATH = "config/default.yaml"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="Snake",
        description="Play Snake",
    )
    parser.add_argument(
        "--config",
        "-c",
        metavar="CONFIG_FILE",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file. If not provided, uses the default config.",
    )

    return parser.parse_args()


def process_config_path(config_path: str) -> str:
    """Process the config path."""
    variant = [
        config_path,
        f"config/{config_path}",
        f"config/{config_path}.yaml",
        f"{config_path}.yaml",
    ]
    for path in variant:
        if os.path.exists(path) and os.path.isfile(path):
            return path
    raise FileNotFoundError(f"Config file {config_path} not found.")


if __name__ == "__main__":
    # Check if the log directory exist if not make it
    if not os.path.exists("log"):
        os.mkdir("log")

    # Define a logger with default parameters
    logger = logging.getLogger(__name__)
    logging.basicConfig(**LOGGING_CONFIG)
    logger.info("Starting run.py")

    # Parse the command line arguments
    args = parse_args()
    config_path = process_config_path(args.config)

    logger.info(f"Using config file {config_path}")

    # Launch the app with the given config path
    app = App(config_path)
    app.run()