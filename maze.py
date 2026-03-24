from collections import deque
from cell import Cell

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

    # --- GENERATION HELPERS (Ignoring Walls) ---
    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        neighbors = []
        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((direction, self.grid[ny][nx]))
        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        return [
            (direction, neighbor)
            for direction, neighbor in self.get_neighbors(cell)
            if not neighbor.visited
        ]

    def remove_wall(self, current: Cell, direction: str, neighbor: Cell) -> None:
        opposite = {"N": "S", "E": "W", "S": "N", "W": "E"}
        current.walls[direction] = False
        neighbor.walls[opposite[direction]] = False

    # --- ENTRY / EXIT LOGIC ---
    def set_entry_exit(self, entry: tuple[int, int], exit_coord: tuple[int, int]) -> None:
        ex, ey = entry
        tx, ty = exit_coord

        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError(f"Entry out of bounds: {entry}")
        if not (0 <= tx < self.width and 0 <= ty < self.height):
            raise ValueError(f"Exit out of bounds: {exit_coord}")
        if entry == exit_coord:
            raise ValueError("Entry and exit cannot be the same")

        self.entry = entry
        self.exit = exit_coord

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

    # --- SOLVING LOGIC (Respecting Walls) ---
    def get_accessible_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        x, y = cell.x, cell.y
        if not cell.walls["N"] and y > 0:
            neighbors.append(self.grid[y - 1][x])
        if not cell.walls["S"] and y < self.height - 1:
            neighbors.append(self.grid[y + 1][x])
        if not cell.walls["W"] and x > 0:
            neighbors.append(self.grid[y][x - 1])
        if not cell.walls["E"] and x < self.width - 1:
            neighbors.append(self.grid[y][x + 1])
        return neighbors

    def find_shortest_path(self) -> str:
        if self.entry is None or self.exit is None:
            raise ValueError("Entry and exit must be set")

        start = self.get_cell(*self.entry)
        end = self.get_cell(*self.exit)

        queue = deque([start])
        parent: dict[Cell, Cell | None] = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                break
            for neighbor in self.get_accessible_neighbors(current):
                if neighbor not in parent:
                    parent[neighbor] = current
                    queue.append(neighbor)

        if end not in parent:
            raise ValueError("No path found from entry to exit")

        # Subject requires returning the path as a string of "N, E, S, W"
        path_str = ""
        current = end
        while parent[current] is not None:
            prev = parent[current]
            dx, dy = current.x - prev.x, current.y - prev.y
            
            if dy == -1: path_str += "N"
            elif dx == 1: path_str += "E"
            elif dy == 1: path_str += "S"
            elif dx == -1: path_str += "W"
            
            current = prev

        return path_str[::-1] # Reverse the string since we traced from exit to entry


    def apply_42_pattern(self) -> None:
        # A minimalist 4 and 2 (1 means closed cell, 0 means open)
        # Dimensions: 5 rows high. '4' is 3 wide, space is 1 wide, '2' is 3 wide. Total = 7 cols.
        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        p_height = len(pattern)
        p_width = len(pattern[0])

        # Subject requirement: Omit if maze is too small 
        # We need at least 1 cell of padding around the pattern so the path can go around it
        if self.width < p_width + 2 or self.height < p_height + 2:
            print("Warning: Maze size too small to draw the '42' pattern.")
            return

        # Calculate offset to center the pattern in the maze
        offset_x = (self.width - p_width) // 2
        offset_y = (self.height - p_height) // 2

        # Apply the mask
        for py in range(p_height):
            for px in range(p_width):
                if pattern[py][px] == 1:
                    cell = self.get_cell(offset_x + px, offset_y + py)
                    cell.is_pattern = True
                    cell.visited = True # The generator will ignore it!