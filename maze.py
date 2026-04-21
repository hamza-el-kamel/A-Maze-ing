from collections import deque
from mazegen import Cell


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = []
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.patern: tuple[int, int] | None = None

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def set_entry_exit(
        self, entry: tuple[int, int], exit_coord: tuple[int, int]
    ) -> None:
        entry_x, entry_y = entry
        exit_x, exit_y = exit_coord

        if not (0 <= entry_x < self.width and 0 <= entry_x < self.height):
            raise ValueError(f"Entry out of bounds: {entry}")
        if not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
            raise ValueError(f"Exit out of bounds: {exit_coord}")

        if self.patern:
            if self.grid[entry_y][entry_x].is_pattern:
                raise ValueError(
                    f"Entry {entry} cannot be inside the 42 pattern wall"
                )
            if self.grid[exit_y][exit_x].is_pattern:
                raise ValueError(
                    f"Exit {exit_coord} cannot be inside the 42 pattern wall"
                )

        if entry == exit_coord:
            raise ValueError("Entry and exit cannot be the same")

        self.entry = entry
        self.exit = exit_coord

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

        path_str = ""
        while True:
            prev = parent[current]
            if prev is None:
                break
            dx, dy = current.x - prev.x, current.y - prev.y

            if dy == -1:
                path_str += "N"
            elif dx == 1:
                path_str += "E"
            elif dy == 1:
                path_str += "S"
            elif dx == -1:
                path_str += "W"

            current = prev

        return path_str[::-1]
