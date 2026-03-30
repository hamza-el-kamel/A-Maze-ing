import os
import time
from generator import MazeGenerator
from exporter import export_maze

# ==============================
# CONFIG & ASSETS
# ==============================

# Converted from sets {...} to lists [...] so we can index them!
# Enable ANSI (important for Windows)
os.system("")

# ===== ANSI COLORS =====
RESET = "\033[0m"

BLACK_BG = "\033[40m"
WHITE = "\033[37m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"

# ===== KEEP EMOJIS (player + target ONLY) =====
ENTRY_ICONS = ["🧍", "🚀", "🚗"]
TARGET_ICONS = ["🏆", "🎯", "🏁"]

# ===== ANSI PATH (no emojis) =====
PATH_ICONS = [YELLOW + "⚪" + RESET, YELLOW + "🟢" + RESET, YELLOW + "🔴" + RESET]

# ===== ANSI WALLS (maze style) =====
WALL_ICONS = [
    WHITE + "██" + RESET,  # theme 1
    GREEN + "██" + RESET,  # theme 2
    RED + "██" + RESET,  # theme 3
]

# ===== BLACK BACKGROUND =====
OPEN = BLACK_BG + "  " + RESET

# The names of your themes to show in the menu
THEME_NAMES = ["City Walk (Black)", "Flight Path (Green)", "Emergency (Red)"]

# ==============================
# CORE DISPLAY
# ==============================


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_maze(maze, path=None, player_pos=None, theme_index=0) -> None:
    clear_screen()

    # Grab the current icons for the selected theme
    current_entry = ENTRY_ICONS[theme_index]
    current_target = TARGET_ICONS[theme_index]
    current_path = PATH_ICONS[theme_index]
    current_wall = WALL_ICONS[theme_index]

    render_w = maze.width * 2 + 1
    render_h = maze.height * 2 + 1
    grid = [[True for _ in range(render_w)] for _ in range(render_h)]

    # 1. Carve out the cells and open walls
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            rx, ry = x * 2 + 1, y * 2 + 1

            # --- THE FIX IS HERE ---
            # If the cell is part of the 42, make its center a solid wall!
            if hasattr(cell, "is_pattern") and cell.is_pattern:
                grid[ry][rx] = True
            else:
                # Normal cells have an open center
                grid[ry][rx] = False

            # Carve walls if they are open
            if not cell.walls["N"]:
                grid[ry - 1][rx] = False
            if not cell.walls["S"]:
                grid[ry + 1][rx] = False
            if not cell.walls["W"]:
                grid[ry][rx - 1] = False
            if not cell.walls["E"]:
                grid[ry][rx + 1] = False

    # 2. Map path coordinates to the new render grid
    render_path = set()
    if path:
        for i in range(len(path)):
            px, py = path[i]
            render_path.add((px * 2 + 1, py * 2 + 1))
            if i > 0:
                prev_x, prev_y = path[i - 1]
                rx = (px + prev_x) + 1
                ry = (py + prev_y) + 1
                render_path.add((rx, ry))

    # 3. Print the high-res grid
    for y in range(render_h):
        for x in range(render_w):
            orig_x, orig_y = (x - 1) // 2, (y - 1) // 2
            is_cell_center = x % 2 != 0 and y % 2 != 0

            # Draw entities using the current theme
            if is_cell_center and player_pos == (orig_x, orig_y):
                # The moving "head" of the path during animation
                print(current_entry, end="")
            elif is_cell_center and maze.entry == (orig_x, orig_y):
                # Permanently show the start icon at the entrance
                print(current_entry, end="")
            elif is_cell_center and maze.exit == (orig_x, orig_y):
                # Permanently show the target icon at the exit
                print(current_target, end="")
            elif (x, y) in render_path:
                print(current_path, end="")
            elif grid[y][x]:
                print(current_wall, end="")
            else:
                print(OPEN, end="")
        print()
    print()


def animate_solution(maze, path, theme_index, delay: float = 0.08) -> None:
    visited = []
    for pos in path:
        visited.append(pos)
        display_maze(maze, path=visited, player_pos=pos, theme_index=theme_index)
        time.sleep(delay)


# ==============================
# HELPERS & INTERACTIVE LOOP
# ==============================


def string_path_to_coords(maze, path_str: str) -> list[tuple[int, int]]:
    if not maze.entry:
        return []

    x, y = maze.entry
    coords = [(x, y)]

    for move in path_str:
        if move == "N":
            y -= 1
        elif move == "S":
            y += 1
        elif move == "E":
            x += 1
        elif move == "W":
            x -= 1

        coords.append((x, y))

    return coords


def run_interactive_menu(maze, config) -> None:
    path_str = maze.find_shortest_path()
    path_coords = string_path_to_coords(maze, path_str)

    show_path = False
    theme_index = 0
    try:
        while True:
            # Display the maze based on current state and theme
            active_path = path_coords if show_path else None
            display_maze(maze, path=active_path, theme_index=theme_index)

            # Print Menu dynamically based on the current theme
            current_theme_name = THEME_NAMES[theme_index]
            current_entry_icon = ENTRY_ICONS[theme_index]
            current_target_icon = TARGET_ICONS[theme_index]

            print("====== A-Maze-ing Interactive Menu ======")
            print("1. Re-generate a new maze")
            print(f"2. {'Hide' if show_path else 'Show'} path from entry to exit")
            print(f"3. Rotate maze theme (Current: {current_theme_name})")
            print(f"4. Animate solution {current_entry_icon} to {current_target_icon}")
            print("5. Quit")

            choice = input("\nChoice? (1-5): ").strip()
            # In display.py inside run_interactive_menu()

            if choice == "1":
                # 1. Reset the maze grid and walls
                maze.__init__(config["WIDTH"], config["HEIGHT"])
                maze.set_entry_exit(config["ENTRY"], config["EXIT"])

                # 2. Generate the new maze structure
                gen = MazeGenerator(maze, perfect=config["PERFECT"])
                gen.generate()

                # 3. FIX: Recalculate the path for the NEW maze
                new_path_str = maze.find_shortest_path()
                path_coords = string_path_to_coords(maze, new_path_str)

                # 4. Optional: Export the new maze to the file
                export_maze(maze, config["OUTPUT_FILE"], new_path_str)

                print("\nMaze re-generated successfully!")

            elif choice == "2":
                show_path = not show_path

            elif choice == "3":
                # Rotate through the themes using modulo arithmetic
                theme_index = (theme_index + 1) % len(THEME_NAMES)
                show_path = False

            elif choice == "4":
                animate_solution(maze, path_coords, theme_index)
                show_path = True

            elif choice == "5":
                print("\nExiting A-Maze-ing. Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")
                time.sleep(1)
    except (KeyboardInterrupt, Exception):
        print("\n\nInterrupted by user. Exiting gracefully...")
