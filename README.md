*This project has been created as part of the 42 curriculum by elhamza sasaidi*

# 🧩 A-Maze-ing

## 📖 Description

This project is a maze generator written in Python.

The goal is to create a random maze using a configuration file, save it in a file, and display it visually.
The maze can also show the shortest path from the entry to the exit.


## ⚙️ Instructions

### ▶️ Run the program

python3 a_maze_ing.py config.txt

### 📦 Install dependencies

make install

### ▶️ Run

make run

### 🧹 Clean files

make clean

### 🔍 Check code

make lint


## 📚 Resources

* Python documentation
* Maze generation algorithms, and solve of it tutorials (DFS, BFS).

### 🤖 AI Usage

AI was used to:

* Understand some algorithms
* Help with documentation


## 📝 Configuration File

The config file uses this format:

```
KEY=VALUE
```

### Required keys:

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True


🧠 Maze Algorithm

This project uses two algorithms:

DFS (Depth-First Search) → used to generate the maze
BFS (Breadth-First Search) → used to find the shortest path from entry to exit

❓ Why These Algorithms
DFS: Easy to implement, Creates good random mazes, Can generate a perfect maze (one unique path)
BFS: Finds the shortest path , Guarantees the best solution from entry to exit

## ♻️ Reusable Code

The maze generator is implemented in a separate class:

```
MazeGenerator
```

### You can:

* Create a maze with custom size
* Use a seed for reproducibility
* Get the maze structure
* Get the solution path

### Example:

```python
generator = MazeGenerator(width=10, height=10)
maze = generator.generate()
```

## 👥 Team & Project Management

### 👤 Roles

* elhamza : Parsing, Display .
* sasaidi : DFS, BFS .
### 📅 Planning

* Started with basic maze generation
* Added configuration file
* Added visualization and pathfinding

### ✅ What worked well

* Good structure of the code
* Clear separation of logic

### ❌ What can be improved

* Better UI
* More algorithms

### 🛠 Tools

* Git / GitHub
* Python
* Makefile


## ✨ Extra Features

*  Maze animation during generation
*  Shortest path display
*  Random seed support
*  Visual maze display
