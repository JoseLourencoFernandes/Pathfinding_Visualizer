import heapq
import random
from definitions.states import State
from classes.grid import Grid
from classes.graph import Graph

class Algorithm:
    """
    Abstract base class for pathfinding algorithms.
    This class provides a common interface for all pathfinding algorithms,
    including methods for resetting the algorithm, stepping through the algorithm,
    and highlighting the path found.
    
    :param structure: The grid or graph structure on which the algorithm operates.
    :type structure: Grid or Graph
    :param get_neighbors: A callable that returns the neighbors of a given node.
    :type get_neighbors: callable
    :param queue: A list to manage the nodes to be processed by the algorithm.
    :type queue: list
    :param visited: A set to keep track of visited nodes.
    :type visited: set
    :param parents: A dictionary mapping each node to its parent node.
    :type parents: dict
    :param path: A list to store the path found by the algorithm.
    :type path: list
    :param found: A flag indicating whether the goal has been found.
    :type found: bool
    """
    structure: Grid | Graph
    get_neighbors: callable
    queue: list
    visited: set
    parents: dict
    path: list
    found: bool

    def __init__(self, structure: Graph | Grid, get_neighbors: callable) -> None:
        """ Constructor for the Algorithm class. """
        self.structure = structure
        self.get_neighbors = get_neighbors
        self.reset()


    def reset(self) -> None:
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
    
    def step(self) -> None:
        """
        Executes a single step of the algorithm.
        This method should be implemented by subclasses to define the specific
        behavior of the algorithm.
        
        :return: A boolean indicating whether the algorithm can continue processing.
        :rtype: bool
        
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
    
    def highlight_path(self) -> None:
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
            parent = self.parents.get(node)
            if not node.state.is_start() and not node.state.is_goal():
                node.change_state(State.PATH)
            if parent is not None and hasattr(self.structure, "mark_edge_path"):
                self.structure.mark_edge_path(node, parent)
            self.path.append(node)
            node = self.parents.get(node) 


class BFSAlgorithm(Algorithm):
    """
    Breadth-First Search (BFS) algorithm for pathfinding.
    This class implements the BFS algorithm to find the shortest path
    from the start square to the goal square in the grid.
    """
    def __init__(self, structure: Graph | Grid, get_neighbors: callable) -> None:
        super().__init__(structure, get_neighbors)

    def reset(self) -> None:
        super().reset()
        self.queue = []
        start = self.structure.get_start()
        if start:
            self.queue.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self) -> None:
        if not self.queue or self.found:
            return False  # end processing
        node = self.queue.pop(0)
        parent = self.parents.get(node)
        if parent is not None and hasattr(self.structure, "mark_edge_visited"):
            self.structure.mark_edge_visited(parent, node)
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
                if hasattr(self.structure, "mark_edge_frontier"):
                    self.structure.mark_edge_frontier(node, neighbor)
        return True  # continue processing


class DFSAlgorithm(Algorithm):
    """
    Depth-First Search (DFS) algorithm for pathfinding.
    This class implements the DFS algorithm to find a path from the start square
    to the goal square in the grid.
    """
    def __init__(self, structure: Graph | Grid, get_neighbors: callable) -> None:
        super().__init__(structure, get_neighbors)

    def reset(self) -> None:
        super().reset()
        self.stack = []
        start = self.structure.get_start()
        if start:
            self.stack.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self) -> None:
        if not self.stack or self.found:
            return False  # end processing
        node = self.stack.pop()
        parent = self.parents.get(node)
        if parent is not None and hasattr(self.structure, "mark_edge_visited"):
            self.structure.mark_edge_visited(parent, node)
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
                if hasattr(self.structure, "mark_edge_frontier"):
                    self.structure.mark_edge_frontier(node, neighbor)
        return True  # continue processing

import itertools

class DijkstraAlgorithm(Algorithm):
    """
    Dijkstra's algorithm for pathfinding.
    This class implements Dijkstra's algorithm to find the shortest path
    from the start square to the goal square in the grid.
    """
    def __init__(self, structure: Graph | Grid, get_neighbors: callable, get_cost: callable) -> None:
        self.get_cost = get_cost
        super().__init__(structure, get_neighbors)

    def reset(self) -> None:
        super().reset()
        self.heap = []
        self.costs = {}
        self.counter = itertools.count()
        start = self.structure.get_start()
        if start:
            heapq.heappush(self.heap, (0, next(self.counter), start))
            self.visited.add(start)
            self.parents[start] = None
            self.costs[start] = 0

    def step(self) -> None:
        if not self.heap or self.found:
            return False
        cost, _, node = heapq.heappop(self.heap)
        parent = self.parents.get(node)
        if parent is not None and hasattr(self.structure, "mark_edge_visited"):
            self.structure.mark_edge_visited(parent, node)
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for neighbor in self.get_neighbors(node):
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = cost + self.get_cost(node, neighbor)
                if neighbor not in self.costs or new_cost < self.costs[neighbor]:
                    self.costs[neighbor] = new_cost
                    heapq.heappush(self.heap, (new_cost, next(self.counter), neighbor))
                    self.parents[neighbor] = node
                    if neighbor.state.is_goal():
                        self.found = True
                    elif neighbor.state.is_activated():
                        neighbor.change_state(State.FRONTIER)
                    if hasattr(self.structure, "mark_edge_frontier"):
                        self.structure.mark_edge_frontier(node, neighbor)
        return True


class AStarAlgorithm(Algorithm):
    """
    A* algorithm for pathfinding.
    This class implements the A* algorithm to find the shortest path
    from the start square to the goal square in the grid, using a heuristic.
    """
    def __init__(self, structure: Graph | Grid, get_neighbors: callable, get_cost: callable, heuristic: callable) -> None:
        self.get_cost = get_cost
        self.heuristic = heuristic
        super().__init__(structure, get_neighbors)

    def reset(self) -> None:
        super().reset()
        self.heap = []
        self.costs = {}
        self.counter = itertools.count()
        start = self.structure.get_start()
        goal = self.structure.get_goal()
        self.goal = goal
        if start and goal:
            heapq.heappush(self.heap, (0, next(self.counter), start))
            self.visited.add(start)
            self.parents[start] = None
            self.costs[start] = 0

    def step(self) -> None:
        if not self.heap or self.found:
            return False
        priority, _, node = heapq.heappop(self.heap)
        parent = self.parents.get(node)
        if parent is not None and hasattr(self.structure, "mark_edge_visited"):
            self.structure.mark_edge_visited(parent, node)
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for neighbor in self.get_neighbors(node):
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = self.costs[node] + self.get_cost(node, neighbor)
                if neighbor not in self.costs or new_cost < self.costs[neighbor]:
                    self.costs[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, self.goal)
                    heapq.heappush(self.heap, (priority, next(self.counter), neighbor))
                    self.parents[neighbor] = node
                    if neighbor.state.is_goal():
                        self.found = True
                    elif neighbor.state.is_activated():
                        neighbor.change_state(State.FRONTIER)
                    if hasattr(self.structure, "mark_edge_frontier"):
                        self.structure.mark_edge_frontier(node, neighbor)
        return True
    
class GreedyBestFirstAlgorithm(Algorithm):
    """
    Greedy Best-First Search algorithm for pathfinding.
    This class implements the Greedy Best-First Search algorithm to find a path
    from the start square to the goal square in the grid, using a heuristic.
    """
    def __init__(self, structure: Graph | Grid, get_neighbors: callable, heuristic: callable) -> None:
        self.heuristic = heuristic
        super().__init__(structure, get_neighbors)
        
    def reset(self) -> None:
        super().reset()
        self.heap = []
        self.counter = itertools.count()
        start = self.structure.get_start()
        goal = self.structure.get_goal()
        self.goal = goal
        if start and goal:
            heapq.heappush(self.heap, (self.heuristic(start, self.goal), next(self.counter), start))
            self.visited.add(start)
            self.parents[start] = None

    def step(self) -> None:
        if not self.heap or self.found:
            return False
        _, _, node = heapq.heappop(self.heap)
        parent = self.parents.get(node)
        if parent is not None and hasattr(self.structure, "mark_edge_visited"):
            self.structure.mark_edge_visited(parent, node)
        if not node.state.is_start() and not node.state.is_goal():
            node.change_state(State.VISITED)
        for neighbor in self.get_neighbors(node):
            if neighbor not in self.visited and (neighbor.state.is_activated() or neighbor.state.is_goal()):
                heapq.heappush(self.heap, (self.heuristic(neighbor, self.goal), next(self.counter), neighbor))
                self.visited.add(neighbor)
                self.parents[neighbor] = node
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
                if hasattr(self.structure, "mark_edge_frontier"):
                    self.structure.mark_edge_frontier(node, neighbor)
        return True
    
    
def generate_maze_prim(grid: Grid) -> None:
    """
    Generates a maze using Prim's algorithm.
    This function initializes all squares as walls (deactivated) and then
    creates a maze by activating squares in a random manner, ensuring that
    the maze is connected and has no loops.
    
    :param grid: The grid on which the maze will be generated.
    :type grid: Grid
    """

    # Inicialize all squares as walls (deactivated)
    for row in range(grid.height):
        for col in range(grid.width):
            grid.get((row, col)).change_state(State.DEACTIVATED)

    # Choose a random starting point
    start_row = random.randrange(0, grid.height, 2)
    start_col = random.randrange(0, grid.width, 2)
    grid.get((start_row, start_col)).change_state(State.ACTIVATED)

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
            if grid.get((n_row, n_col)).state.is_deactivated():
                # Carve a passage by activating the wall and the neighboring square
                grid.get((wall_row, wall_col)).change_state(State.ACTIVATED)
                grid.get((n_row, n_col)).change_state(State.ACTIVATED)
                # Add the neighboring square's walls to the list
                for d_row, d_col in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nn_row, nn_col = n_row + d_row, n_col + d_col
                    if 0 <= nn_row < grid.height and 0 <= nn_col < grid.width:
                        if grid.get((nn_row, nn_col)).state.is_deactivated():
                            walls.append((n_row + d_row//2, n_col + d_col//2, nn_row, nn_col))
                            