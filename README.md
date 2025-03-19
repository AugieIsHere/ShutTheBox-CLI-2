# ShutTheBox CLI 2

A new and improved command-line implementation of the classic "Shut The Box" dice game with animated visuals and AI opponents.
*Created with [Cursor AI](https://cursor.sh/) by someone who can't code. Feel free to update yourself!*

## About the Game

Shut The Box is a traditional pub game where players roll dice and try to "shut" numbered tiles by matching the sum of their dice rolls. The goal is to shut all tiles; otherwise, the score is the sum of remaining open tiles (lower is better).

## Features

- Colorful ASCII animations and interface
- Single-player mode against AI opponents with multiple difficulty levels
- Advanced mode with sidebar display showing all players' boards
- Option to play with 1 or 2 dice based on game state
- Multiple rounds with cumulative scoring

## How to Play

1. Roll the dice
2. Choose a valid combination of numbers to shut (must equal your dice sum)
3. Continue rolling and shutting numbers until no valid moves remain
4. The game ends when a player shuts all their numbers or has no valid moves
5. Lowest score wins!

## Requirements

- Python 3.6 or higher

## Running the Game

```bash
python dont_shut_the_box.py
```

### Command-line Options

- `-s` or `--skip-intro`: Skip the introduction and game rules screen
- `-sm` or `--simple`: Run the game in simple mode (without advanced sidebar display)

Examples:
```bash
# Skip introduction and run with full UI
python dont_shut_the_box.py -s

# Run in simple mode with basic display
python dont_shut_the_box.py -sm

# Both skip intro and use simple mode
python dont_shut_the_box.py -s -sm
```

---
 
