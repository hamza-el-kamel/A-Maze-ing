import random
from maze import Maze
from cell import Cell

class MazeGenerator:
    def __init__(self, maze: Maze, perfect: bool = True, seed: int | None = None) -> None:
        self.maze = maze
        self.perfect = perfect 
        if seed is not None:
            random.seed(seed)

    def generate(self) -> None:
        self.maze.apply_42_pattern()

        start_cell = None
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if not getattr(self.maze.get_cell(x, y), 'is_pattern', False):
                    start_cell = self.maze.get_cell(x, y)
                    break
            if start_cell:
                break
                
        if not start_cell:
            raise ValueError("Maze is completely filled by the pattern!")

        stack: list[Cell] = []
        start_cell.visited = True
        stack.append(start_cell)

        while stack:
            current = stack[-1]
            neighbors = self.maze.get_unvisited_neighbors(current)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.maze.remove_wall(current, direction, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
                
        if not self.perfect:
            self._make_imperfect()

    def _make_imperfect(self) -> None:
        num_walls_to_remove = (self.maze.width * self.maze.height) // 20 
        removed = 0
        attempts = 0
        max_attempts = num_walls_to_remove * 10

        while removed < num_walls_to_remove and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            cell = self.maze.get_cell(x, y)

            if getattr(cell, 'is_pattern', False):
                continue

            closed_dirs = []
            if cell.walls["N"] and y > 0: closed_dirs.append("N")
            if cell.walls["S"] and y < self.maze.height - 1: closed_dirs.append("S")
            if cell.walls["W"] and x > 0: closed_dirs.append("W")
            if cell.walls["E"] and x < self.maze.width - 1: closed_dirs.append("E")

            if closed_dirs:
                direction = random.choice(closed_dirs)
                nx, ny = x, y
                if direction == "N": ny -= 1
                elif direction == "S": ny += 1
                elif direction == "E": nx += 1
                elif direction == "W": nx -= 1
                
                neighbor = self.maze.get_cell(nx, ny)
                
                if not getattr(neighbor, 'is_pattern', False):
                    self.maze.remove_wall(cell, direction, neighbor)
                    removed += 1