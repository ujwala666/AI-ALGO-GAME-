import heapq
import math
import sys
import pygame

# NEURO ESCAPE: An AI pathfinding maze game
# Install dependency: python -m pip install pygame
# Run: python neuro_escape.py

pygame.init()

CELL = 36
COLS, ROWS = 19, 15
HUD_HEIGHT = 76
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + HUD_HEIGHT
FPS = 60

# # = wall, . = path, P = player start, H = hunter start,
# C = energy crystal, E = exit
LEVEL = [
    "###################",
    "#P....#.....#....C#",
    "#.##..#.###.#.##..#",
    "#....##...#.#.....#",
    "###.####..#...###.#",
    "#...#.....###.....#",
    "#.#.#.###.....##..#",
    "#.#...#...##...#..#",
    "#.#####.#....#.#..#",
    "#.....#.#.##.#....#",
    "#.###...#....####.#",
    "#...###....#......#",
    "##......##...##...E",
    "#C....#.....#....H#",
    "###################",
]

BG = (12, 16, 34)
FLOOR = (22, 29, 55)
WALL = (54, 64, 103)
GRID = (32, 41, 72)
CYAN = (66, 235, 255)
PURPLE = (155, 105, 255)
RED = (255, 76, 112)
GOLD = (255, 207, 76)
WHITE = (238, 242, 255)
MUTED = (156, 169, 202)
GREEN = (92, 245, 164)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEURO ESCAPE | Adaptive AI Maze")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 19, bold=True)
small_font = pygame.font.SysFont("consolas", 14)
big_font = pygame.font.SysFont("consolas", 34, bold=True)


def parse_level():
    walls, crystals = set(), set()
    player = hunter = exit_pos = None
    for y, row in enumerate(LEVEL):
        for x, char in enumerate(row):
            pos = (x, y)
            if char == "#":
                walls.add(pos)
            elif char == "P":
                player = pos
            elif char == "H":
                hunter = pos
            elif char == "C":
                crystals.add(pos)
            elif char == "E":
                exit_pos = pos
    return walls, crystals, player, hunter, exit_pos


def heuristic(a, b):
    """Manhattan distance: estimated moves between two grid cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(pos, walls):
    """Return walkable cells directly above, below, left, and right."""
    x, y = pos
    for nxt in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        nx, ny = nxt
        if 0 <= nx < COLS and 0 <= ny < ROWS and nxt not in walls:
            yield nxt


def a_star(start, goal, walls):
    """
    A* pathfinding.
    g_score = cost so far; h = estimated remaining cost; f = g + h.
    Returns a list of cells from start to goal, or [] if no route exists.
    """
    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    closed = set()

    while frontier:
        _, cost, current = heapq.heappop(frontier)
        if current in closed:
            continue
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed.add(current)
        for nxt in neighbors(current, walls):
            new_cost = g_score[current] + 1
            if new_cost < g_score.get(nxt, math.inf):
                g_score[nxt] = new_cost
                came_from[nxt] = current
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, new_cost, nxt))
    return []


def cell_center(pos):
    x, y = pos
    return x * CELL + CELL // 2, HUD_HEIGHT + y * CELL + CELL // 2


def draw_text(text, x, y, color=WHITE, chosen_font=font):
    image = chosen_font.render(text, True, color)
    screen.blit(image, (x, y))


def reset_game():
    walls, crystals, player, hunter, exit_pos = parse_level()
    return {
        "walls": walls,
        "crystals": crystals,
        "player": player,
        "hunter": hunter,
        "exit": exit_pos,
        "score": 0,
        "status": "playing",
        "hunter_timer": 0.0,
        "player_timer": 0.0,
        "path": [],
        "message": "",
    }


def draw_game(game):
    screen.fill(BG)
    draw_text("NEURO ESCAPE", 16, 14, CYAN, big_font)
    draw_text(f"CRYSTALS: {len(game['crystals'])}   SCORE: {game['score']}", 18, 52, WHITE, small_font)
    if game["crystals"]:
        draw_text("Collect every crystal to unlock the exit!", 300, 24, GOLD, small_font)
    else:
        draw_text("EXIT UNLOCKED  ->", 300, 24, GREEN, small_font)

    # Maze tiles
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL, HUD_HEIGHT + y * CELL, CELL, CELL)
            if (x, y) in game["walls"]:
                pygame.draw.rect(screen, WALL, rect, border_radius=5)
                pygame.draw.rect(screen, (77, 90, 137), rect, 1, border_radius=5)
            else:
                pygame.draw.rect(screen, FLOOR, rect)
                pygame.draw.rect(screen, GRID, rect, 1)

    # Show the hunter's current A* route
    if len(game["path"]) > 1 and game["status"] == "playing":
        points = [cell_center(p) for p in game["path"]]
        if len(points) > 1:
            pygame.draw.lines(screen, (71, 80, 142), False, points, 3)

    # Exit
    ex, ey = game["exit"]
    exit_rect = pygame.Rect(ex * CELL + 5, HUD_HEIGHT + ey * CELL + 5, CELL - 10, CELL - 10)
    exit_color = GREEN if not game["crystals"] else (104, 109, 137)
    pygame.draw.rect(screen, exit_color, exit_rect, border_radius=8)
    draw_text("E", ex * CELL + 12, HUD_HEIGHT + ey * CELL + 8, BG)

    # Crystals
    for crystal in game["crystals"]:
        cx, cy = cell_center(crystal)
        points = [(cx, cy - 9), (cx + 8, cy), (cx, cy + 9), (cx - 8, cy)]
        pygame.draw.polygon(screen, GOLD, points)
        pygame.draw.polygon(screen, WHITE, points, 1)

    # Player
    px, py = cell_center(game["player"])
    pygame.draw.circle(screen, CYAN, (px, py), 12)
    pygame.draw.circle(screen, WHITE, (px - 3, py - 3), 3)

    # AI hunter
    hx, hy = cell_center(game["hunter"])
    pygame.draw.circle(screen, RED, (hx, hy), 13)
    pygame.draw.circle(screen, (255, 205, 215), (hx - 4, hy - 3), 3)
    pygame.draw.circle(screen, (255, 205, 215), (hx + 4, hy - 3), 3)

    draw_text("Move: WASD / Arrows     Restart: R     Quit: Esc", 15, HEIGHT - 24, MUTED, small_font)

    if game["status"] != "playing":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 7, 20, 190))
        screen.blit(overlay, (0, 0))
        title = "YOU ESCAPED!" if game["status"] == "won" else "THE AI CAUGHT YOU!"
        color = GREEN if game["status"] == "won" else RED
        title_img = big_font.render(title, True, color)
        screen.blit(title_img, title_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        sub_img = font.render("Press R to play again", True, WHITE)
        screen.blit(sub_img, sub_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 28)))

    pygame.display.flip()


def main():
    game = reset_game()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = reset_game()
                elif game["status"] == "playing":
                    dx = dy = 0
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        dx = -1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        dx = 1
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        dy = -1
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        dy = 1

                    if dx or dy:
                        target = (game["player"][0] + dx, game["player"][1] + dy)
                        if target not in game["walls"]:
                            game["player"] = target
                            if target in game["crystals"]:
                                game["crystals"].remove(target)
                                game["score"] += 10
                            if target == game["exit"] and not game["crystals"]:
                                game["status"] = "won"

        if game["status"] == "playing":
            # Recalculate A* path to the player's current position.
            game["path"] = a_star(game["hunter"], game["player"], game["walls"])

            # The hunter moves more quickly as the player collects crystals.
            # The shorter interval means a faster hunter.
            hunter_interval = max(0.16, 0.48 - game["score"] * 0.006)
            game["hunter_timer"] += dt
            if game["hunter_timer"] >= hunter_interval:
                game["hunter_timer"] = 0.0
                if len(game["path"]) > 1:
                    game["hunter"] = game["path"][1]

            if game["hunter"] == game["player"]:
                game["status"] = "lost"

        draw_game(game)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
