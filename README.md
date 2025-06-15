# Pathfinding Visualizer

A Python project using **Pygame** to visualize different searching algorithms in a 2D grid. Users can interactively create obstacles, define a **start** and **goal** point, and watch the algorithm explore the grid. There are **two grid modes**: normal grid and weighted grid. 

## Features
- Main menu with mode selection
  - Normal Grid
  - Weighted Grid (using costs)
- Interactive 2D grid creation
- Start and goal point selection
- Obstacle placement
- Visualization of various pathfinding algorithms
  - BFS
  - DFS
  - A*
  - Dijkstra
  - Greedy Best-First Search
- Maze generation (using Prim's algorithm)
- Real-time animation using **Pygame**
- Execution time tracking for algorithms
- **Custom costs** support via file input

## Installation

```bash
git clone https://github.com/JoseLourencoFernandes/Pathfinding_Visualizer.git
cd Pathfinding_Visualizer
```

## Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

## Install dependencies:
```
pip install -r requirements.txt
```

## Requirements
 - Python 3.x
 - Pygame 2.6.1

## Usage
```
python main.py
```

## Controls:

### General
- Left-click to create obstacles
- Right-click to remove obstacles
- Use UI buttons to set **start** and **goal** points
- Select an algorithm to watch it in action
- Press the **Maze button** to generate a randomized maze (using Prim's algorithm)
  
### Reset
- **Reset button**:  
  - First click → *partial reset* (restores the previously generated grid)  
  - Second click → *full reset* (clears everything)  

### Keyboard Shortcuts
- `Ctrl + R` → Full reset  
- `Ctrl + Q` → Quit application
- `ESC` → Returns to main menu

## Using Weighted Grids (costs.txt)
The Weighted Grid mode requires a file named costs.txt, formatted as follows (e.g. of a 3x3 grid):
```
6 5 1
1 8 5
2 8 1
```
Each line represents a row of the grid, with numbers indicating the cost of each cell.

### Generating a costs.txt file automatically:
You can generate a random **costs.txt** file using the following script:
```
python generate_costs.py
```

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/

