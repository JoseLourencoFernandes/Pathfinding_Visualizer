import pygame
from definitions.grid_constants import SQUARE_SIZE, SPACING
from definitions.colors import Color
from definitions.states import State
from utils.loaders import load_grid_costs


class Square:
    """
    A class to represent a square in the grid.
    This class handles the square's position, size, and state.
    It provides methods to draw the square on a screen and change its state.
    
    Attributes:
        x (int): The x-coordinate of the square's top-left corner.
        y (int): The y-coordinate of the square's top-left corner.
        size (int): The size of the square (width and height).
        state (State): The current state of the square, represented by the State Enum.
        cost (int): The cost of the square (used for pathfinding algorithms).

    Methods:
        draw(screen): Draws the square on the given screen based on its state.
        change_state(new_state): Changes the state of the square to a new state.
    """
    def __init__(self, x, y, size, state, cost=0):
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        self.cost = cost
        self.row = y // (size + SPACING)  # Calculate row based on y position
        self.col = x // (size + SPACING)
        self.cost_surface = None # Cache for cost surface to avoid re-rendering
        
    def get_cost_surface(self):
        """
        Returns the cost surface for the square, rendering it if not already cached.
        
        Returns:
            pygame.Surface: The surface containing the cost text.
        """
        if self.cost_surface is None:
            #Font size is 90% of the square size, at least 10 pixels
            font_size = max(10, int(self.size * 0.9))
            font = pygame.font.Font(None, font_size)
            self.cost_surface = font.render(str(self.cost), True, Color.BLACK)
        return self.cost_surface

    def draw(self, screen, show_cost=False):
        """
        Draws the square on the given screen based on its state.
        
        Arguments:
            screen: The screen on which to draw the square.
        """
        if (self.state.is_deactivated()):
            pygame.draw.rect(screen, Color.BROWN, (self.x, self.y, self.size, self.size))
        elif (self.state.is_activated()):
            pygame.draw.rect(screen, Color.GRAY, (self.x, self.y, self.size, self.size))
            if show_cost:
                self.draw_cost(screen)
        elif (self.state.is_start()):
            pygame.draw.rect(screen, Color.GREEN, (self.x, self.y, self.size, self.size))
        elif (self.state.is_goal()):
            pygame.draw.rect(screen, Color.RED, (self.x, self.y, self.size, self.size))
        elif (self.state.is_visited()):
            pygame.draw.rect(screen, Color.PALEGREEN, (self.x, self.y, self.size, self.size))
            if show_cost:
                self.draw_cost(screen)
        elif (self.state.is_path()):
            pygame.draw.rect(screen, Color.LIGHTBLUE, (self.x, self.y, self.size, self.size))
            if show_cost:
                self.draw_cost(screen)
        elif (self.state.is_frontier()):
            pygame.draw.rect(screen, Color.ORANGE, (self.x, self.y, self.size, self.size))
            if show_cost:
                self.draw_cost(screen)
    
    def draw_cost(self, screen):
        """
        Draws the cost of the square on the screen.
        This method retrieves the cost surface and blits it onto the screen at the square's center.

        Arguments:
            screen: The screen on which to draw the cost.
        """
        surface = self.get_cost_surface()
        text_rect = surface.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        screen.blit(surface, text_rect)
            
    def change_state(self, new_state):
        """
        Changes the state of the square to a new state.
        
        Arguments:
            new_state (State): The new state to set for the square.
        
        Raises:
            ValueError: If new_state is not an instance of State Enum.
        """
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of State Enum")

        self.state = new_state


class Grid:
    """
    A class to represent a grid of squares.
    This class initializes a grid of squares based on the specified width, height, square size, and spacing.
    It provides methods to get a square by its row and column, draw the grid on a screen,
    get the start and goal positions, and change the state of a square.
    
    Attributes:
        width (int): The number of columns in the grid.
        height (int): The number of rows in the grid.
        grid (list): A 2D list representing the grid of squares.
        
    Methods:
        get(row, col): Returns the square at the specified row and column.
        draw(screen): Draws the entire grid on the given screen.
        get_start(): Returns the position of the start square as a tuple (row, col).
        get_goal(): Returns the position of the goal square as a tuple (row, col).
        change_state(row, col, new_state): Changes the state of the square at the specified row and column.
    """
    def __init__(self, width, height, square_size=SQUARE_SIZE, spacing=SPACING, state=State.ACTIVATED, customizable_cost = False, offset=0):
        self.width = width
        self.height = height
        self.customizable_cost = customizable_cost
        self.grid = []
        
        # If customizable_costs is True, load costs from file
        costs = []
        if customizable_cost:
            costs = load_grid_costs('costs.txt')
            # Check if the costs file matches the grid dimensions
            if len(costs) != height or any(len(row) != width for row in costs):
                raise ValueError("Costs file dimensions do not match grid dimensions")
            
            
        # Iterate through the height and width to create the grid
        # If costs are not provided, use a default cost of 1 for all squares
        for row in range(height):
            row_list = []
            for col in range(width):
                x = offset + spacing + col * (square_size + spacing)
                y = offset + spacing + row * (square_size + spacing)
                cost = costs[row][col] if customizable_cost else 1
                row_list.append(Square(x, y, square_size, state, cost))
            self.grid.append(row_list)
    
    def get(self, pos):
        """
        Returns the square at the specified position.

        Arguments:
            pos (tuple): A tuple (row, col) representing the position of the square.
            
        REturns:
            Square: The square at the specified position.
            
        Raises:
            ValueError: If pos is not a tuple of length 2.
            IndexError: If the row or column index is out of bounds.
        """
        
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise ValueError("Position must be a tuple (row, col)")
        
        if not (0 <= pos[0] < self.height and 0 <= pos[1] < self.width):
            raise IndexError("Row or column index out of bounds")
        return self.grid[pos[0]][pos[1]]

    def draw(self, screen):
        """
        Draws the entire grid on the given screen.
        
        Arguments:
            screen: The screen on which to draw the grid.
        """
        for row in self.grid:
            for square in row:
                square.draw(screen, self.customizable_cost)

    def get_start(self):
        """
        Returns the position of the start square as a tuple (row, col) or None if not found.
        
        Returns:
            Square: The square representing the start position, or None if not found.
        """
        for row in self.grid:
            for square in row:
                if square.state.is_start():
                    return square
        return None
    
    def get_goal(self):
        """
        Returns the position of the goal square as a tuple (row, col) or None if not found.
        
        Returns:
            tuple: A tuple (row, col) representing the position of the goal square, or None if not found.
        """
        for row in self.grid:
            for square in row:
                if square.state.is_goal():
                    return square
        return None

    def change_state(self, row, col, new_state):
        """
        Changes the state of the square at the specified row and column.
        
        Arguments:
            row (int): The row index of the square.
            col (int): The column index of the square.
            new_state (State): The new state to set for the square.
            
        Raises:
            ValueError: If new_state is not an instance of State Enum.
        """
        # Validate new_state is an instance of State Enum
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of State Enum")

        # Validate row and col indices
        if not (0 <= row < self.height and 0 <= col < self.width):
            raise IndexError("Row or column index out of bounds")

        # Change the state of the square at (row, col)
        # Ensures that exists only one start and one goal square at a time
        if new_state.is_start():
            start_pos = self.get_start()
            if start_pos is not None:
                start_pos.change_state(State.ACTIVATED)
            self.grid[row][col].change_state(State.START)
        elif new_state.is_goal():
            goal_pos = self.get_goal()
            if goal_pos is not None:
                goal_pos.change_state(State.ACTIVATED)
            self.grid[row][col].change_state(State.GOAL)

        # Ensures that if activating a square that is currently the start,
        # it will change to ACTIVATED state instead of START state
        elif new_state.is_activated():
            if self.grid[row][col].state.is_start():
                self.grid[row][col].change_state(State.ACTIVATED)
            else:
                self.grid[row][col].change_state(new_state)
                
        # For all other states, just change the state
        else:
            self.grid[row][col].change_state(new_state)
            
    def get_neighbors(self, square):
        """
        Returns the valid neighbors of a given square in the grid.
        This method yields the coordinates of the neighboring squares
        that are within the bounds of the grid.
        
        Arguments:
            row (int): The row index of the square.
            col (int): The column index of the square.
            
        Yields:
            tuple: A tuple (n_row, n_col) representing the coordinates of a neighboring square.
        """
        for d_row, d_col in [(-1,0),(1,0),(0,-1),(0,1)]:
            n_row, n_col = square.row + d_row, square.col + d_col
            if 0 <= n_row < self.height and 0 <= n_col < self.width:
                yield self.grid[n_row][n_col]
                
    def get_cost(self, node, neighbor):
        """
        Returns the cost of moving from one square to its neighbor.
        
        Arguments:
            node (Square): The current square.
            neighbor (Square): The neighboring square.
            
        Returns:
            int: The cost of moving from node to neighbor.
        """
        return neighbor.cost
                
def manhattan_heuristic(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col)
