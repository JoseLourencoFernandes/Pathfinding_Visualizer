import heapq
import random
from definitions.states import State


class Algorithm:
    """
    Abstract base class for pathfinding algorithms.
    This class provides a common interface for all pathfinding algorithms,
    including methods for resetting the algorithm, stepping through the algorithm,
    and highlighting the path found.
    
    Attributes:
        structure (Grid or Graph): The grid or graph structure on which the algorithm operates.
        visited (set): A set of visited nodes.
        parents (dict): A dictionary mapping each node to its parent node.
        path (list): A list to store the path found by the algorithm.
        found (bool): A flag indicating whether the goal has been found.
    """
    def __init__(self, structure, get_neighbors):
        self.structure = structure
        self.get_neighbors = get_neighbors
        self.reset()


    def reset(self):
        """
        Resets the algorithm state.
        This method clears the visited nodes, parents mapping, path list,
        and the found flag.
        """
        self.queue = []
        self.visited = set()
        self.parents = {}
        self.path = []
        self.found = False
    
    def step(self):
        """
        Executes a single step of the algorithm.
        This method should be implemented by subclasses to define the specific
        behavior of the algorithm.
        
        Returns:
            bool: True if the algorithm can continue processing, False if it has completed.
        """
        raise NotImplementedError
    
    def highlight_path(self):
        """
        Highlights the path found by the algorithm.
        This method traces back from the goal node to the start node,
        changing the state of each square in the path to State.PATH.
        If the goal node is not found, it does nothing.
        """
        goal = self.structure.get_goal()
        if not goal:
            return
        node = goal
        while node is not None:
            if not node.state.is_start() and not node.state.is_goal():
                node.change_state(State.PATH)
            self.path.append(node)
            node = self.parents.get(node) 


class BFSAlgorithm(Algorithm):
    """
    Breadth-First Search (BFS) algorithm for pathfinding.
    This class implements the BFS algorithm to find the shortest path
    from the start square to the goal square in the grid.
    """ 
    def __init__(self, structure, get_neighbors):
        super().__init__(structure, get_neighbors)

    def reset(self):
        super().reset()
        self.queue = []
        start = self.structure.get_start()
        if start:
            self.queue.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self):
        if not self.queue or self.found:
            return False  # end processing
        node = self.queue.pop(0)
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for neighbor in self.get_neighbors(node):
            if neighbor not in self.visited and (neighbor.state.is_activated() or neighbor.state.is_goal()):
                self.queue.append(neighbor)
                self.visited.add(neighbor)
                self.parents[neighbor] = node
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
        return True  # continue processing


class DFSAlgorithm(Algorithm):
    """
    Depth-First Search (DFS) algorithm for pathfinding.
    This class implements the DFS algorithm to find a path from the start square
    to the goal square in the grid.
    """
    def __init__(self, structure, get_neighbors):
        super().__init__(structure, get_neighbors)

    def reset(self):
        super().reset()
        self.stack = []
        start = self.structure.get_start()
        if start:
            self.stack.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self):
        if not self.stack or self.found:
            return False  # end processing
        node = self.stack.pop()
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for neighbor in self.structure.get_neighbors(node):
            if neighbor not in self.visited and (neighbor.state.is_activated() or neighbor.state.is_goal()):
                self.stack.append(neighbor)
                self.visited.add(neighbor)
                self.parents[neighbor] = node
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
        return True  # continue processing


class DijkstraAlgorithm(Algorithm):
    """
    Dijkstra's algorithm for pathfinding.
    This class implements Dijkstra's algorithm to find the shortest path
    from the start square to the goal square in the grid.
    """
    def __init__(self, structure, get_neighbors):
        super().__init__(structure, get_neighbors)

    def reset(self):
        super().reset()
        self.heap = []
        self.costs = {}
        start = self.structure.get_start()
        if start:
            heapq.heappush(self.heap, (0, start))
            self.visited.add(start)
            self.parents[start] = None
            self.costs[start] = 0

    def step(self):
        if not self.heap or self.found:
            return False
        cost, (row, col) = heapq.heappop(self.heap)
        square = self.structure.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.structure.get(n_row, n_col)
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = cost + neighbor.cost
                if (n_row, n_col) not in self.costs or new_cost < self.costs[(n_row, n_col)]:
                    self.costs[(n_row, n_col)] = new_cost
                    heapq.heappush(self.heap, (new_cost, (n_row, n_col)))
                    self.parents[(n_row, n_col)] = (row, col)
                    if neighbor.state.is_goal():
                        self.found = True
                    elif neighbor.state.is_activated():
                        neighbor.change_state(State.FRONTIER)
        return True


class AStarAlgorithm(Algorithm):
    """
    A* algorithm for pathfinding.
    This class implements the A* algorithm to find the shortest path
    from the start square to the goal square in the grid, using a heuristic.
    """
    def __init__(self, grid):
        super().__init__(grid)

    def reset(self):
        super().reset()
        self.heap = []
        self.costs = {}
        start = self.structure.get_start()
        goal = self.structure.get_goal()
        self.goal = goal
        if start and goal:
            heapq.heappush(self.heap, (0, start))
            self.visited.add(start)
            self.parents[start] = None
            self.costs[start] = 0

    def heuristic(self, node):
        # Manhattan distance
        if not self.goal:
            return 0
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def step(self):
        if not self.heap or self.found:
            return False
        cost, (row, col) = heapq.heappop(self.heap)
        square = self.structure.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.structure.get(n_row, n_col)
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = self.costs[(row, col)] + neighbor.cost
                if (n_row, n_col) not in self.costs or new_cost < self.costs[(n_row, n_col)]:
                    self.costs[(n_row, n_col)] = new_cost
                    priority = new_cost + self.heuristic((n_row, n_col))
                    heapq.heappush(self.heap, (priority, (n_row, n_col)))
                    self.parents[(n_row, n_col)] = (row, col)
                    if neighbor.state.is_goal():
                        self.found = True
                    elif neighbor.state.is_activated():
                        neighbor.change_state(State.FRONTIER)
        return True
    
    
class GreedyBestFirstAlgorithm(Algorithm):
    """
    Greedy Best-First Search algorithm for pathfinding.
    This class implements the Greedy Best-First Search algorithm to find a path
    from the start square to the goal square in the grid, using a heuristic.
    """
    def __init__(self, structure, get_neighbors):
        super().__init__(structure, get_neighbors)

    def reset(self):
        super().reset()
        self.heap = []
        start = self.structure.get_start()
        goal = self.structure.get_goal()
        self.goal = goal
        if start and goal:
            heapq.heappush(self.heap, (self.heuristic(start), start))
            self.visited.add(start)
            self.parents[start] = None

    def heuristic(self, node):
        # Manhattan distance
        if not self.goal:
            return 0
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def step(self):
        if not self.heap or self.found:
            return False
        _, node = heapq.heappop(self.heap)
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(node):
            neighbor = self.structure.get(n_row, n_col)
            if (n_row, n_col) not in self.visited and (neighbor.state.is_activated() or neighbor.state.is_goal()):
                heapq.heappush(self.heap, (self.heuristic((n_row, n_col)), (n_row, n_col)))
                self.visited.add((n_row, n_col))
                self.parents[(n_row, n_col)] = (node.row, node.col)
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
        return True
    
    
def generate_maze_prim(grid):
    """
    Generates a maze using Prim's algorithm.
    This function initializes all squares as walls (deactivated) and then
    creates a maze by activating squares in a random manner, ensuring that
    the maze is connected and has no loops.
    
    Arguments:
        grid (Grid): The grid on which the maze will be generated.
    """

    # Inicialize all squares as walls (deactivated)
    for row in range(grid.height):
        for col in range(grid.width):
            grid.get(row, col).change_state(State.DEACTIVATED)

    # Choose a random starting point
    start_row = random.randrange(0, grid.height, 2)
    start_col = random.randrange(0, grid.width, 2)
    grid.get(start_row, start_col).change_state(State.ACTIVATED)

    # List of walls to be processed, it will contain tuples of the form (wall_row, wall_col, n_row, n_col)
    # where (n_row, n_col) is the neighbor of the wall
    # and (wall_row, wall_col) is the wall that separates the two squares
    walls = []
    
    # Add initial walls around the starting point
    for d_row, d_col in [(-2,0),(2,0),(0,-2),(0,2)]:
        n_row, n_col = start_row + d_row, start_col + d_col
        if 0 <= n_row < grid.height and 0 <= n_col < grid.width:
            walls.append((start_row + d_row//2, start_col + d_col//2, n_row, n_col))

    # Process walls until there are no more walls to process
    while walls:
        # Choose a random wall from the list
        idx = random.randrange(len(walls))
        wall_row, wall_col, n_row, n_col = walls.pop(idx)
        # Check if the wall is valid (i.e., it separates two squares)
        if 0 <= n_row < grid.height and 0 <= n_col < grid.width:
            # Check if the neighboring square is deactivated
            if grid.get(n_row, n_col).state.is_deactivated():
                # Carve a passage by activating the wall and the neighboring square
                grid.get(wall_row, wall_col).change_state(State.ACTIVATED)
                grid.get(n_row, n_col).change_state(State.ACTIVATED)
                # Add the neighboring square's walls to the list
                for d_row, d_col in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nn_row, nn_col = n_row + d_row, n_col + d_col
                    if 0 <= nn_row < grid.height and 0 <= nn_col < grid.width:
                        if grid.get(nn_row, nn_col).state.is_deactivated():
                            walls.append((n_row + d_row//2, n_col + d_col//2, nn_row, nn_col))
                            