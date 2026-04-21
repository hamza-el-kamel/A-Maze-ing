import random


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.walls = {"N": True, "E": True, "S": True, "W": True}
        self.visited = False
        self.is_pattern = False


class MazeGenerator:
    def __init__(
        self, width: int,
        height: int,
        perfect: bool = True,
        seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        self.patern: tuple[int, int] | None = None
        random.seed(seed)
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        neighbors = []
        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))
        return neighbors

    def remove_wall(self,
                    current: Cell,
                    direction: str,
                    neighbor: Cell) -> None:
        opposite = {"N": "S", "E": "W", "S": "N", "W": "E"}
        current.walls[direction] = False
        neighbor.walls[opposite[direction]] = False

    def apply_42_pattern(self) -> None:
        pattern_map = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        p_height = len(pattern_map)
        p_width = len(pattern_map[0])
        self.patern = (p_width, p_height)

        if self.width < p_width + 2 or self.height < p_height + 2:
            print("Error: Maze size too small to draw the '42' pattern.")
            return

        offset_x = (self.width - p_width) // 2
        offset_y = (self.height - p_height) // 2

        for py in range(p_height):
            for px in range(p_width):
                if pattern_map[py][px] == 1:
                    cell = self.get_cell(offset_x + px, offset_y + py)
                    cell.is_pattern = True
                    cell.visited = True

    def first_free_cell(self) -> Cell | None:
        for y in range(self.height):
            for x in range(self.width):
                if not self.get_cell(x, y).is_pattern:
                    return self.get_cell(x, y)
        return None

    def generate(self) -> None:
        self.apply_42_pattern()

        # Find the first non-pattern cell to start DFS from
        start_cell = self.first_free_cell()

        if not start_cell:
            raise ValueError("Maze is completely filled by the pattern!")

        # DFS (depth first search)
        stack = [start_cell]
        start_cell.visited = True

        while stack:
            current = stack[-1]
            neighbors = self.get_neighbors(current)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.remove_wall(current, direction, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.perfect:
            self.make_imperfect()

    def open_walls_count(self, cell: "Cell") -> int:
        return sum(1 for wall in cell.walls.values() if not wall)

    def make_imperfect(self, prob: float = 0.50) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.is_pattern:
                    continue

                directions = []
                if y > 0 and cell.walls["N"]:
                    directions.append("N")
                if y < self.height - 1 and cell.walls["S"]:
                    directions.append("S")
                if x > 0 and cell.walls["W"]:
                    directions.append("W")
                if x < self.width - 1 and cell.walls["E"]:
                    directions.append("E")

                if directions and random.random() < prob:
                    direction = random.choice(directions)
                    nx, ny = x, y
                    if direction == "N":
                        ny -= 1
                    elif direction == "S":
                        ny += 1
                    elif direction == "E":
                        nx += 1
                    elif direction == "W":
                        nx -= 1

                    neighbor = self.get_cell(nx, ny)

                    if (
                        self.open_walls_count(cell) > 2
                        or self.open_walls_count(neighbor) > 2
                    ):
                        continue

                    if not neighbor.is_pattern:
                        self.remove_wall(cell, direction, neighbor)
