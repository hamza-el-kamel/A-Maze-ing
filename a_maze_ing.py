import sys
from parse import parse_config
from maze import Maze
from generator import MazeGenerator
from exporter import export_maze
from display import run_interactive_menu

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        config = parse_config(sys.argv[1])
        maze = Maze(config["WIDTH"], config["HEIGHT"])
        maze.set_entry_exit(config["ENTRY"], config["EXIT"])
        
        gen = MazeGenerator(maze, perfect=config["PERFECT"])
        gen.generate()

        path_str = maze.find_shortest_path()
        export_maze(maze, config["OUTPUT_FILE"], path_str)
        run_interactive_menu(maze, config)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()