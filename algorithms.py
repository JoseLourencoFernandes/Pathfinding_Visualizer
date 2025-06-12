import heapq
from definitions import State

# Algorithm classes
class Algorithm:
    def __init__(self, grid):
        self.grid = grid
        self.reset()

    def reset(self):
        self.visited = set()
        self.parents = {}
        self.path = []
        self.found = False
    
    def step(self):
        raise NotImplementedError
    
    def highlight_path(self):
        goal = self.grid.get_goal()
        if not goal:
            return
        node = goal
        while node is not None:
            row, col = node
            square = self.grid.get(row, col)
            if not square.state.is_start() and not square.state.is_goal():
                square.change_state(State.PATH)
            self.path.append(node)
            node = self.parents.get(node) 
            
    def _get_neighbors(self, row, col):
        # returns neighbors of a square in the grid
        for d_row, d_col in [(-1,0),(1,0),(0,-1),(0,1)]:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < self.grid.height and 0 <= n_col < self.grid.width:
                yield n_row, n_col


class BFSAlgorithm(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def reset(self):
        super().reset()
        self.queue = []
        start = self.grid.get_start()
        if start:
            self.queue.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self):
        if not self.queue or self.found:
            return False  # end processing
        row, col = self.queue.pop(0)
        square = self.grid.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.grid.get(n_row, n_col)
            if (n_row, n_col) not in self.visited and neighbor.state.is_activated() or neighbor.state.is_goal():
                self.queue.append((n_row, n_col))
                self.visited.add((n_row, n_col))
                self.parents[(n_row, n_col)] = (row, col)
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
        return True  # continue processing


class DFSAlgorithm(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def reset(self):
        super().reset()
        self.stack = []
        start = self.grid.get_start()
        if start:
            self.stack.append(start)
            self.visited.add(start)
            self.parents[start] = None

    def step(self):
        if not self.stack or self.found:
            return False  # end processing
        row, col = self.stack.pop()
        square = self.grid.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.grid.get(n_row, n_col)
            if (n_row, n_col) not in self.visited and neighbor.state.is_activated() or neighbor.state.is_goal():
                self.stack.append((n_row, n_col))
                self.visited.add((n_row, n_col))
                self.parents[(n_row, n_col)] = (row, col)
                if neighbor.state.is_goal():
                    self.found = True
                elif neighbor.state.is_activated():
                    neighbor.change_state(State.FRONTIER)
        return True  # continue processing


class DijkstraAlgorithm(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
        
    def reset(self):
        super().reset()
        self.heap = []
        self.costs = {}
        start = self.grid.get_start()
        if start:
            heapq.heappush(self.heap, (0, start))
            self.visited.add(start)
            self.parents[start] = None
            self.costs[start] = 0

    def step(self):
        if not self.heap or self.found:
            return False
        cost, (row, col) = heapq.heappop(self.heap)
        square = self.grid.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.grid.get(n_row, n_col)
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = cost + 1  # ou outro custo se quiseres pesos
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
    def __init__(self, grid):
        super().__init__(grid)

    def reset(self):
        super().reset()
        self.heap = []
        self.costs = {}
        start = self.grid.get_start()
        goal = self.grid.get_goal()
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
        square = self.grid.get(row, col)
        if not square.state.is_start() and not square.state.is_goal():
            square.change_state(State.VISITED)
        for n_row, n_col in self._get_neighbors(row, col):
            neighbor = self.grid.get(n_row, n_col)
            if neighbor.state.is_activated() or neighbor.state.is_goal():
                new_cost = self.costs[(row, col)] + 1  # or use a different cost if needed
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