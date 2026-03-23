import random
import sys
from collections import deque
import pygame

sys.setrecursionlimit(10000)

# ═══════════════════════════════
# Colors
# ═══════════════════════════════
BLACK      = (0,   0,   0)
WALL_COLOR = (180, 140, 0)
PATH_COLOR = (0,   180, 200)
ENTRY_COL  = (255, 0,   255)
EXIT_COL   = (255, 0,   0)
BG_COLOR   = (0,   0,   0)

COLORS_LIST = [
    (180, 140, 0),
    (255, 255, 255),
    (0,   100, 255),
    (0,   200, 0),
    (180, 0,   180),
    (0,   220, 220),
    (255, 60,  60),
]

CELL_SIZE  = 20
WALL_THICK = 3


# ═══════════════════════════════
# Maze Generator
# ═══════════════════════════════
class MazeGenerator:
    def __init__(self, width, height, entry, exit_pos, perfect=True, seed=None):
        self.width    = width
        self.height   = height
        self.entry    = entry
        self.exit_pos = exit_pos
        self.perfect  = perfect
        self.seed     = seed

        if seed is not None:
            random.seed(seed)

        self.grid = [
            [{'N': True, 'E': True, 'S': True, 'W': True}
             for _ in range(width)]
            for _ in range(height)
        ]

    def generate_maze(self):
        visited  = [[False] * self.width for _ in range(self.height)]
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        def dfs(x, y):
            visited[y][x] = True
            directions = ['N', 'E', 'S', 'W']
            random.shuffle(directions)
            for d in directions:
                nx, ny = x, y
                if d == 'N': ny -= 1
                elif d == 'S': ny += 1
                elif d == 'E': nx += 1
                elif d == 'W': nx -= 1
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and not visited[ny][nx]):
                    self.grid[y][x][d] = False
                    self.grid[ny][nx][opposite[d]] = False
                    dfs(nx, ny)

        ex, ey = self.entry
        dfs(ex, ey)

    def solve(self):
        start   = self.entry
        end     = self.exit_pos
        queue   = deque([(start, [])])
        visited = {start}
        delta   = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
                return path
            for d, (dx, dy) in delta.items():
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and not self.grid[y][x][d]
                        and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [d]))
        return []


# ═══════════════════════════════
# Draw
# ═══════════════════════════════
def draw_maze(screen, maze, wall_color, show_path, path, offset_x, offset_y):
    path_cells = set()
    if show_path and path:
        x, y = maze.entry
        path_cells.add((x, y))
        delta = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
        for d in path:
            dx, dy = delta[d]
            x += dx
            y += dy
            path_cells.add((x, y))

    screen.fill(BLACK)

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            px   = offset_x + x * CELL_SIZE
            py   = offset_y + y * CELL_SIZE

            if (x, y) == maze.entry:
                pygame.draw.rect(screen, ENTRY_COL,
                                 (px+1, py+1, CELL_SIZE-1, CELL_SIZE-1))
            elif (x, y) == maze.exit_pos:
                pygame.draw.rect(screen, EXIT_COL,
                                 (px+1, py+1, CELL_SIZE-1, CELL_SIZE-1))
            elif show_path and (x, y) in path_cells:
                pygame.draw.rect(screen, PATH_COLOR,
                                 (px+1, py+1, CELL_SIZE-1, CELL_SIZE-1))

            if cell['N']:
                pygame.draw.line(screen, wall_color,
                                 (px, py), (px + CELL_SIZE, py), WALL_THICK)
            if cell['S']:
                pygame.draw.line(screen, wall_color,
                                 (px, py + CELL_SIZE),
                                 (px + CELL_SIZE, py + CELL_SIZE), WALL_THICK)
            if cell['W']:
                pygame.draw.line(screen, wall_color,
                                 (px, py), (px, py + CELL_SIZE), WALL_THICK)
            if cell['E']:
                pygame.draw.line(screen, wall_color,
                                 (px + CELL_SIZE, py),
                                 (px + CELL_SIZE, py + CELL_SIZE), WALL_THICK)

    pygame.display.flip()


def draw_menu(screen, font, wall_color, show_path, color_idx, W, H):
    menu_y = H - 30
    pygame.draw.rect(screen, (20, 20, 20), (0, menu_y, W, 30))
    text = f"1:regen  2:path({'ON' if show_path else 'OFF'})  3:color  4:quit"
    surf = font.render(text, True, (200, 200, 200))
    screen.blit(surf, (10, menu_y + 5))
    pygame.display.flip()


# ═══════════════════════════════
# Config
# ═══════════════════════════════
def read_config(filepath):
    config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    return config


# ═══════════════════════════════
# Main
# ═══════════════════════════════
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python a_maze_ing.py config.txt")
        sys.exit(1)

    config   = read_config(sys.argv[1])
    width    = int(config['WIDTH'])
    height   = int(config['HEIGHT'])
    entry    = tuple(map(int, config['ENTRY'].split(',')))
    exit_pos = tuple(map(int, config['EXIT'].split(',')))
    perfect  = config.get('PERFECT', 'True') == 'True'

    pygame.init()
    font      = pygame.font.SysFont('consolas', 14)
    OFFSET_X  = 10
    OFFSET_Y  = 10
    WIN_W     = width  * CELL_SIZE + OFFSET_X * 2
    WIN_H     = height * CELL_SIZE + OFFSET_Y * 2 + 35
    screen    = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("A-Maze-ing")

    maze       = MazeGenerator(width, height, entry, exit_pos, perfect)
    maze.generate_maze()
    path       = []
    show_path  = False
    color_idx  = 0
    wall_color = COLORS_LIST[color_idx]

    draw_maze(screen, maze, wall_color, show_path, path, OFFSET_X, OFFSET_Y)
    draw_menu(screen, font, wall_color, show_path, color_idx, WIN_W, WIN_H)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    maze = MazeGenerator(width, height, entry, exit_pos, perfect)
                    maze.generate_maze()
                    path      = []
                    show_path = False
                    draw_maze(screen, maze, wall_color, show_path, path,
                              OFFSET_X, OFFSET_Y)

                elif event.key == pygame.K_2:
                    if not path:
                        path = maze.solve()
                    show_path = not show_path
                    draw_maze(screen, maze, wall_color, show_path, path,
                              OFFSET_X, OFFSET_Y)

                elif event.key == pygame.K_3:
                    color_idx  = (color_idx + 1) % len(COLORS_LIST)
                    wall_color = COLORS_LIST[color_idx]
                    draw_maze(screen, maze, wall_color, show_path, path,
                              OFFSET_X, OFFSET_Y)

                elif event.key == pygame.K_4:
                    running = False

                draw_menu(screen, font, wall_color, show_path,
                          color_idx, WIN_W, WIN_H)

    pygame.quit()
    sys.exit()