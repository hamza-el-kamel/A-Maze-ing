import random
from maze import Maze
from cell import Cell
from collections import deque

class MazeGenerator:
    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        self.maze = maze
        if seed is not None:
            random.seed(seed)

    def generate(self) -> None:
        # 1. Burn the 42 pattern into the grid first
        self.maze.apply_42_pattern()

        # 2. Find a valid starting cell (can't be part of the 42)
        start_cell = None
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if not self.maze.get_cell(x, y).is_pattern:
                    start_cell = self.maze.get_cell(x, y)
                    break
            if start_cell:
                break
                
        if not start_cell:
            raise ValueError("Maze is completely filled by the pattern!")

        # 3. Standard Recursive Backtracker
        stack: list[Cell] = []
        start_cell.visited = True
        stack.append(start_cell)

        while stack:
            current = stack[-1]
            neighbors = self.maze.get_unvisited_neighbors(current)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                # Remove wall between current and next
                self.maze.remove_wall(current, direction, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                # Dead end → backtrack
                stack.pop()
class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]
    
def set_entry_exit(self, entry: tuple[int, int], exit: tuple[int, int]) -> None:
    ex, ey = entry
    tx, ty = exit

    # Bounds validation
    if not (0 <= ex < self.width and 0 <= ey < self.height):
        raise ValueError(f"Entry out of bounds: {entry}")

    if not (0 <= tx < self.width and 0 <= ty < self.height):
        raise ValueError(f"Exit out of bounds: {exit}")

    # Must be different
    if entry == exit:
        raise ValueError("Entry and exit cannot be the same")

    self.entry = entry
    self.exit = exit

def open_entry_exit(self) -> None:
    if self.entry is None or self.exit is None:
        raise ValueError("Entry/Exit must be set before opening")

    self._open_border(self.entry, "Entry")
    self._open_border(self.exit, "Exit")

def _open_border(self, pos: tuple[int, int], label: str) -> None:
    x, y = pos
    cell = self.get_cell(x, y)

    if y == 0:
        cell.walls["N"] = False
    elif y == self.height - 1:
        cell.walls["S"] = False
    elif x == 0:
        cell.walls["W"] = False
    elif x == self.width - 1:
        cell.walls["E"] = False
    else:
        raise ValueError(f"{label} must be on maze border: {pos}")
    
def validate_maze(self) -> None:
    for row in self.grid:
        for cell in row:
            # Check for isolated cell (all walls closed)
            if all(cell.walls.values()):
                raise ValueError(f"Isolated cell at ({cell.x}, {cell.y})")
            
def validate_walls(self) -> None:
    for y in range(self.height):
        for x in range(self.width):
            cell = self.grid[y][x]

            # East neighbor
            if x + 1 < self.width:
                neighbor = self.grid[y][x + 1]
                if cell.walls["E"] != neighbor.walls["W"]:
                    raise ValueError(f"Inconsistent wall between ({x},{y}) and ({x+1},{y})")

            # South neighbor
            if y + 1 < self.height:
                neighbor = self.grid[y + 1][x]
                if cell.walls["S"] != neighbor.walls["N"]:
                    raise ValueError(f"Inconsistent wall between ({x},{y}) and ({x},{y+1})")
    
def get_neighbors(self, cell: Cell) -> list[Cell]:
    neighbors = []
    x, y = cell.x, cell.y

    # North
    if not cell.walls["N"] and y > 0:
        neighbors.append(self.grid[y - 1][x])

    # South
    if not cell.walls["S"] and y < self.height - 1:
        neighbors.append(self.grid[y + 1][x])

    # West
    if not cell.walls["W"] and x > 0:
        neighbors.append(self.grid[y][x - 1])

    # East
    if not cell.walls["E"] and x < self.width - 1:
        neighbors.append(self.grid[y][x + 1])

    return neighbors

def find_shortest_path(self) -> list[tuple[int, int]]:
    if self.entry is None or self.exit is None:
        raise ValueError("Entry and exit must be set")

    start = self.get_cell(*self.entry)
    end = self.get_cell(*self.exit)

    queue = deque([start])
    visited = set()
    parent: dict[Cell, Cell | None] = {}

    visited.add(start)
    parent[start] = None

    while queue:
        current = queue.popleft()

        if current == end:
            break

        for neighbor in self.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # Reconstruct path
    path = []
    current = end

    if current not in parent:
        raise ValueError("No path found from entry to exit")

    while current is not None:
        path.append((current.x, current.y))
        current = parent[current]

    path.reverse()
    return path