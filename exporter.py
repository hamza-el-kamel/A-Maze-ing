from maze import Maze


def export_maze(maze: Maze, filename: str, path_str: str) -> None:
    try:
        with open(filename, "w") as f:
            for y in range(maze.height):
                row_hex = ""
                for x in range(maze.width):
                    cell = maze.get_cell(x, y)
                    val = 0
                    if cell.walls["N"]:
                        val |= 1
                    if cell.walls["E"]:
                        val |= 2
                    if cell.walls["S"]:
                        val |= 4
                    if cell.walls["W"]:
                        val |= 8
                    row_hex += f"{val:X}"

                f.write(row_hex + "\n")
            f.write("\n")
            if maze.entry and maze.exit:
                f.write(f"{maze.entry[0]},{maze.entry[1]}\n")
                f.write(f"{maze.exit[0]},{maze.exit[1]}\n")

            f.write(path_str + "\n")

    except IOError as e:
        raise IOError(f"Failed to write to {filename}: {e}")
