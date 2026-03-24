class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        # All walls are initially present
        self.walls: dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }

        self.visited: bool = False
        self.is_pattern: bool = False  # NEW: Tracks if this cell is part of the "42"

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"