# Viva Preparation — NEURO ESCAPE

## Short project explanation
“Neuro Escape is a 2D maze game developed using Python and Pygame. The player collects energy crystals and reaches the exit while an AI hunter pursues the player. The hunter uses the A* pathfinding algorithm to choose a short route through the maze. The game also increases the hunter's speed as the player's score increases.”

## Common viva questions

1. **What is the aim of the project?**  
   To build an interactive game that demonstrates AI-based pathfinding.

2. **What is artificial intelligence in this project?**  
   The hunter uses a search algorithm to choose its next move instead of moving randomly.

3. **Which algorithm is used?**  
   A* (A-star) search.

4. **How does A* work?**  
   It prioritizes cells using `f(n) = g(n) + h(n)`, combining the cost so far with an estimate of the remaining cost.

5. **What is `g(n)`?**  
   The actual number of moves from the starting cell to the current cell.

6. **What is `h(n)`?**  
   An estimate of the remaining distance to the goal. This game uses Manhattan distance.

7. **What is Manhattan distance?**  
   `abs(x1 - x2) + abs(y1 - y2)`. It fits a grid where movement is horizontal or vertical.

8. **Why use `heapq`?**  
   It provides a priority queue so the next cell with the smallest estimated total cost can be selected efficiently.

9. **What does a wall do in pathfinding?**  
   Wall cells are excluded from the hunter's possible next moves.

10. **Is this machine learning?**  
    No. A* is a classical AI search algorithm. The speed adjustment is rule-based adaptation, not a trained learning model.

11. **What is Pygame?**  
    A Python library for creating games, handling keyboard events, drawing graphics, and controlling the game loop.

12. **How is the score calculated?**  
    Each energy crystal collected adds 10 points.

13. **How does the game end?**  
    The player wins by collecting every crystal and reaching the exit, or loses if the hunter reaches the player's cell.

14. **What are the limitations?**  
    The maze is fixed, the hunter follows a predictable shortest-path strategy, and the game does not train a machine-learning model.

15. **What can be improved?**  
    Random levels, multiple enemy strategies, high-score storage, performance metrics, and a comparison of A* with BFS.

## Demonstration checklist
- Run the game and show movement.
- Collect at least one crystal and show the score.
- Point out the route drawn for the hunter.
- Explain `g`, `h`, and `f`.
- Show that the exit unlocks only after all crystals are collected.
- Demonstrate a win or loss and restart.
