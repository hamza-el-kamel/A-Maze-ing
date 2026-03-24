import os
import time
from generator import MazeGenerator
from exporter import export_maze

# ==============================
# CONFIG & ASSETS
# ==============================

CAT = "🚶🏻‍➡️"
GOAL = "🧕🏻"
PATH_CHAR = "🔵" # Changed to a blue circle so it pops against the white!
WALL = "⬛"
OPEN = "⬜"

# ANSI Color Codes for the path (since emojis ignore terminal text colors)
COLORS = [
    ("\033[94m", "Blue"),
    ("\033[92m", "Green"),
    ("\033[91m", "Red"),
    ("\033[95m", "Magenta"),
    ("\033[93m", "Yellow")
]
RESET = "\033[0m"

# ==============================
# CORE DISPLAY
# ==============================

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def display_maze(maze, path=None, player_pos=None, path_color="\033[94m") -> None:
    clear_screen()

    # To use solid blocks, we double the resolution of the grid
    # True = Wall, False = Open Space
    render_w = maze.width * 2 + 1
    render_h = maze.height * 2 + 1
    grid = [[True for _ in range(render_w)] for _ in range(render_h)]

    # 1. Carve out the cells and open walls
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            rx, ry = x * 2 + 1, y * 2 + 1

            # The cell itself is open space
            grid[ry][rx] = False

            # Carve walls if they are open
            if not cell.walls["N"]: grid[ry - 1][rx] = False
            if not cell.walls["S"]: grid[ry + 1][rx] = False
            if not cell.walls["W"]: grid[ry][rx - 1] = False
            if not cell.walls["E"]: grid[ry][rx + 1] = False

    # 2. Map path coordinates to the new render grid
    render_path = set()
    if path:
        for i in range(len(path)):
            px, py = path[i]
            render_path.add((px * 2 + 1, py * 2 + 1))
            # Fill the space between current and previous path step
            if i > 0:
                prev_x, prev_y = path[i-1]
                rx = (px + prev_x) + 1  
                ry = (py + prev_y) + 1
                render_path.add((rx, ry))

    # 3. Print the high-res grid
    for y in range(render_h):
        for x in range(render_w):
            orig_x, orig_y = (x - 1) // 2, (y - 1) // 2
            is_cell_center = (x % 2 != 0 and y % 2 != 0)

            # Draw entities, path, walls, or empty space
            if is_cell_center and player_pos == (orig_x, orig_y):
                print(CAT, end="")
            elif is_cell_center and maze.exit == (orig_x, orig_y):
                print(GOAL, end="")
            elif (x, y) in render_path:
                print(f"{path_color}{PATH_CHAR}{RESET}", end="")
            elif grid[y][x]:
                print(WALL, end="")
            else:
                print(OPEN, end="")
        print() # Newline at end of row
    print()


def animate_solution(maze, path, path_color, delay: float = 0.08) -> None:
    visited = []
    for pos in path:
        visited.append(pos)
        display_maze(maze, path=visited, player_pos=pos, path_color=path_color)
        time.sleep(delay)

# ==============================
# HELPERS & INTERACTIVE LOOP
# ==============================

def string_path_to_coords(maze, path_str: str) -> list[tuple[int, int]]:
    """Converts the 'NNES' string back into (x,y) tuples for the visualizer."""
    if not maze.entry:
        return []
        
    x, y = maze.entry
    coords = [(x, y)]
    
    for move in path_str:
        if move == "N": y -= 1
        elif move == "S": y += 1
        elif move == "E": x += 1
        elif move == "W": x -= 1
            
        coords.append((x, y))
        
    return coords


def run_interactive_menu(maze, config) -> None:
    path_str = maze.find_shortest_path()
    path_coords = string_path_to_coords(maze, path_str)
    
    show_path = False
    color_index = 0
    
    while True:
        current_color = COLORS[color_index][0]
        
        # Display the maze based on current state
        active_path = path_coords if show_path else None
        display_maze(maze, path=active_path, path_color=current_color)
        
        # Print Menu
        print("====== A-Maze-ing Interactive Menu ======")
        print("1. Re-generate a new maze")
        print(f"2. {'Hide' if show_path else 'Show'} path from entry to exit")
        print(f"3. Rotate path colors (Current: {COLORS[color_index][1]})")
        print("4. Animate solution 🐱🐟")
        print("5. Quit")
        
        choice = input("\nChoice? (1-5): ").strip()
        
        if choice == "1":
            maze.__init__(config["WIDTH"], config["HEIGHT"])
            maze.set_entry_exit(config["ENTRY"], config["EXIT"])
            gen = MazeGenerator(maze)
            gen.generate()
            maze.open_entry_exit()
            
            path_str = maze.find_shortest_path()
            path_coords = string_path_to_coords(maze, path_str)
            export_maze(maze, config["OUTPUT_FILE"], path_str)
            
        elif choice == "2":
            show_path = not show_path
            
        elif choice == "3":
            color_index = (color_index + 1) % len(COLORS)
            
        elif choice == "4":
            animate_solution(maze, path_coords, current_color)
            
        elif choice == "5":
            print("\nExiting A-Maze-ing. Goodbye!")
            break
            
        else:
            print("Invalid choice, please try again.")
            time.sleep(1)