*This project has been created as partof the 42 curriculum by elhamza, sasaidi*

## 📌 Description

This project is a **maze generator written in Python**. It reads a configuration file, generates a valid maze (perfect or not), and exports it into a file using a hexadecimal wall encoding.

---

## ⚙️ Instructions

### ▶️ Installation

```bash
make install
```

### ▶️ Run the program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### 🐞 Debug mode

```bash
make debug
```

### 🧹 Clean project

```bash
make clean
```

### 🔍 Lint & type check

```bash
make lint
```

---

## 📄 Configuration File Format

Each line must follow:

```
KEY=VALUE
```

### Required keys:

| Key         | Description      | Example              |
| ----------- | ---------------- | -------------------- |
| WIDTH       | Maze width       | WIDTH=20             |
| HEIGHT      | Maze height      | HEIGHT=15            |
| ENTRY       | Entry position   | ENTRY=0,0            |
| EXIT        | Exit position    | EXIT=19,14           |
| OUTPUT_FILE | Output file name | OUTPUT_FILE=maze.txt |
| PERFECT     | Perfect maze     | PERFECT=True         |

### Example:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

---

## 🧠 Maze Generation Algorithm

We use the **Recursive Backtracking algorithm**:

* Starts from a cell
* Randomly explores neighbors
* Backtracks when stuck

### ✔ Why this algorithm?

* Simple to implement
* Produces perfect mazes naturally
* Guarantees full connectivity
* Efficient for medium/large grids

---

## 🔁 Reusable Code

The maze generator is implemented as a reusable class:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, seed=42)
maze.generate()

grid = maze.get_grid()
path = maze.solve()
```

### Reusable features:

* Maze generation
* Access to structure
* Pathfinding solution

---

## 📦 Packaging

The reusable module is packaged as:

```
mazegen-1.0.0-py3-none-any.whl
```

It can be installed with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

---

## 🎨 Features

* Random maze generation
* Perfect / non-perfect maze
* Shortest path calculation
* ASCII visualization
* “42” pattern generation
* Error handling (invalid config, bounds, etc.)

---

## 📚 Resources

* Maze generation algorithms:

  * https://en.wikipedia.org/wiki/Maze_generation_algorithm
* Recursive Backtracking:

  * https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

### 🤖 AI Usage

AI was used for:

* Structuring the project
* Generating boilerplate code
* Improving documentation
* Debugging ideas

All generated content was reviewed and understood before use.

---

## 👥 Team & Project Management

### Roles

* : Core algorithm & parsing
* : Visualization & output

### Planning

* Initial: Basic generator
* Mid: Add pathfinding + output format
* Final: Add visualization & packaging

### What worked well

* Clear modular structure
* Early testing

### Improvements

* Better time estimation
* More edge case testing

### Tools used

* Git / GitHub
* Python (mypy, flake8)
* Virtualenv

---

## 🚀 Possible Improvements

* Maze animation

---
