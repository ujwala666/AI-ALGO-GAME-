# NEURO ESCAPE — Adaptive AI Maze

A beginner-friendly Python desktop game demonstrating the **A\* pathfinding algorithm**.

## Game idea
You control the cyan player and collect all golden energy crystals. Then reach the green exit. A red AI hunter continually uses A* to find a short walkable path to your current position. The hunter becomes faster as your score increases.

## Requirements
- Python 3.10 or newer recommended
- Pygame

## Run the game
1. Install Python from https://www.python.org/downloads/ if needed.
2. Open Command Prompt / Terminal in this folder.
3. Install Pygame:

   ```bash
   python -m pip install pygame
   ```

4. Start the game:

   ```bash
   python neuro_escape.py
   ```

   On some systems, use `python3` instead of `python`.

## Controls
- Arrow keys or WASD: move
- R: restart
- Esc: quit

## AI algorithm
A* selects a path using:

**f(n) = g(n) + h(n)**

- `g(n)`: exact movement cost from the start to the current cell.
- `h(n)`: Manhattan-distance estimate from the current cell to the target.
- `f(n)`: estimated total cost of a route through the current cell.

The implementation uses a priority queue (`heapq`). Walls are not walkable. Because every move has equal cost and the Manhattan heuristic is suitable for four-direction grid movement, A* can find a shortest path when one exists.

## Current features
- Grid-based maze and keyboard movement
- Energy crystals and scoring
- Exit unlock condition
- AI hunter that recalculates its route
- Increasing enemy speed as score rises
- Win/lose screens and restart

## Suggested future improvements
- Main menu and difficulty selector
- Random maze generation
- High-score saving
- Sound effects and background music
- Multiple levels
- Compare A* with breadth-first search (BFS)
- Add a dashboard showing path length and nodes explored

## Resume bullet (after you have tested it)
**Neuro Escape — AI Pathfinding Game | Python, Pygame, A\***
- Developed a 2D maze game featuring an AI hunter that recalculates routes using A* pathfinding and a Manhattan-distance heuristic.
- Implemented collectible objectives, score-based difficulty scaling, collision detection, and win/lose states.

Only list features you have actually run and verified on your own machine.
