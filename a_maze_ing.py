import sys
from parse import parse_config
from maze import Maze
from mazegen import MazeGenerator
from exporter import export_maze
from display import run_interactive_menu


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    if not sys.argv[1].endswith(".txt"):
        print("The config file must be a .txt file")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    gen = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        perfect=config["PERFECT"],
        seed=config.get("SEED"),
    )
    gen.generate()

    maze = Maze(config["WIDTH"], config["HEIGHT"])
    maze.grid = gen.grid
    maze.patern = gen.patern
    maze.set_entry_exit(config["ENTRY"], config["EXIT"])

    path_str = maze.find_shortest_path()
    export_maze(maze, config["OUTPUT_FILE"], path_str)
    run_interactive_menu(maze, config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
