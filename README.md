# Snake Game

A Python implementation of the classic Snake game with multiple viewing modes and AI strategies.

## Features

- Multiple rendering modes: Console and Pygame
- Configurable game settings (grid size, speed, colors)
- Multiple AI strategies: Player-controlled, Dummy, Cycle
- YAML-based configuration system

## Screenshots

### Console View

![Console View](images/console_view.png)

### Pygame View

![Pygame View](images/pygame_view.png)

## Requirements

- Python >= 3.13
- PyYAML >= 6.0.3
- Pygame >= 2.6.1

## Installation

Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install pyyaml pygame
```

## Usage

Run the game with the default configuration:

```bash
cd project
python run.py
```

Run with a specific configuration:

```bash
python run.py --config console
python run.py --config console_player
python run.py -c default
```

## Configuration

Configuration files are located in the `config/` directory:

- `default.yaml` - Pygame view with player controls
- `console.yaml` - Console view with cycle strategy
- `console_player.yaml` - Console view with player controls

### Configuration Options

- `game.grid_width` / `game.grid_height` - Grid dimensions
- `game.wrap_around` - Enable/disable edge wrapping
- `game.properties.initial_speed` - Starting game speed (milliseconds)
- `game.strategy` - AI strategy (player, dummy, cycle)
- `graphics.enable` - Enable/disable Pygame graphics

## Controls

When using player strategy:

- Arrow keys or ZASD - Move the snake
- ESC - Quit the game

## Project Structure

```
project/
├── config/          # Configuration files
├── src/
│   ├── app.py       # Main application
│   ├── controller/  # Game controllers and input handlers
│   ├── model/       # Game state and snake logic
│   ├── strategies/  # AI strategies
│   └── view/        # Rendering (console and pygame)
└── run.py           # Entry point
```

## License

This project is provided as-is for educational purposes.

