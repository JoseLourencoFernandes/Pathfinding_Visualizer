# Pathfinding Visualizer

A Python project using **Pygame** to visualize different searching algorithms in a 2D grid. Users can interactively create obstacles, define a **start** and **goal** point, and watch the algorithm explore the grid.

## Features

- Interactive 2D grid creation
- Start and goal point selection
- Obstacle placement
- Visualization of various pathfinding algorithms (BFS, DFS, A*, Dijkstra and Greedy-Best-first search)
- Maze generation (using Prim's algorithm)
- Real-time animation using **Pygame**
- Execution time tracking for algorithms

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
- Press designated buttons to set start and goal points
- Choose an algorithm to see its execution
- Press the **Maze button** to generate a randomized maze (using Prim's algorithm)
  
### Reset
- **Reset button**:  
  - First click → *partial reset* (restores the previously generated grid)  
  - Second click → *full reset* (clears everything)  

### Keyboard Shortcuts
- `Ctrl + R` → Full reset  
- `Ctrl + Q` → Quit application

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/

