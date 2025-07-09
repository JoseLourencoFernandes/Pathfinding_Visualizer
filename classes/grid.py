import pygame
from definitions.grid_constants import SQUARE_SIZE, SPACING
from definitions.colors import Color
from definitions.states import State
from utils.loaders import load_grid_costs
from typing import Iterator


class Square:
    """
    A class to represent a square in the grid.
    This class handles the square's position, size, and state.
    It provides methods to draw the square on a screen and change its state.
    
    :param x: The x-coordinate of the square's top-left corner.
    :type x: int
    :param y: The y-coordinate of the square's top-left corner.
    :type y: int
    :param size: The size of the square (width and height).
    :type size: int
    :param state: The current state of the square, represented by the State Enum.
    :type state: State
    :param cost: The cost of the square (used for pathfinding algorithms), defaults to 0.
    :type cost: int, optional  
    :param row: The row index of the square in the grid.
    :type row: int
    :param col: The column index of the square in the grid.
    :type col: int
    :param cost_surface: A cached surface for rendering the cost text, defaults to None.
    :type cost_surface: pygame.Surface, optional
    
    :raises ValueError: If new_state is not an instance of State Enum.
    """
    x: int
    y: int
    size: int
    state: State
    cost: int
    row: int
    col: int
    cost_surface: pygame.Surface

    def __init__(self, x: int, y: int, size: int, state: State, cost: int = 0) -> None:
        """ Constructor for the Square class."""
        if not isinstance(state, State):
            raise ValueError("state must be an instance of State Enum")
        
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        self.cost = cost
        self.row = y // (size + SPACING)  # Calculate row based on y position
        self.col = x // (size + SPACING)  # Calculate column based on x position
        self.cost_surface = None  # Cache for cost surface to avoid re-rendering

    def get_cost_surface(self) -> pygame.Surface:
        """
        Returns the cost surface for the square, rendering it if not already cached.

        :return: The surface containing the cost text.
        """
        if self.cost_surface is None:
            font_size = max(10, int(self.size * 0.9))  # Font size is 90% of the square size, at least 10 pixels
            font = pygame.font.Font(None, font_size)
            self.cost_surface = font.render(str(self.cost), True, Color.BLACK)
        return self.cost_surface

    def draw(self, screen: pygame.Surface, show_cost: bool = False) -> None:
        """
        Draws the square on the given screen based on its state.

        :param screen: The screen on which to draw the square.
        :param show_cost: Whether to display the cost of the square.
        """

        color = self.state.get_color()
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))
        if show_cost and self.state.should_show_cost():
            self.draw_cost(screen)

    
    def draw_cost(self, screen: pygame.Surface) -> None:
        """
        Draws the cost of the square on the screen.
        This method retrieves the cost surface and blits it onto the screen at the square's center.

        :param screen: The screen on which to draw the cost.
        """
        surface = self.get_cost_surface()
        text_rect = surface.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        screen.blit(surface, text_rect)
            
    def change_state(self, new_state: State) -> None:
        """
        Changes the state of the square to a new state.

        :param new_state: The new state to set for the square.
        :type new_state: State
        
        :raises ValueError: If new_state is not an instance of State Enum.
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
    
    :param width: The number of columns in the grid.
    :type width: int
    :param height: The number of rows in the grid.
    :type height: int
    :param grid: A 2D list representing the grid of squares.
    :type grid: list
    :param customizable_cost: Whether the grid allows customizable costs for squares, defaults to False.
    :type customizable_cost: bool
    """
    width: int
    height: int
    grid: list
    customizable_cost: bool

    def __init__(self, width: int, height: int, square_size: int = SQUARE_SIZE, spacing: int = SPACING, state: State = State.ACTIVATED, customizable_cost: bool = False, offset: int = 0) -> None:
        """ Constructor for the Grid class. """
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
    
    def get(self, pos: tuple[int, int]) -> Square:
        """
        Returns the square at the specified position.

        :param pos: A tuple (row, col) representing the position of the square.
        :type pos: tuple[int, int]
        
        :raises ValueError: If pos is not a tuple of length 2.
        :raises IndexError: If the row or column index is out of bounds.
        
        :return: The square at the specified position.
        :rtype: Square
        """
        
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise ValueError("Position must be a tuple (row, col)")
        
        if not (0 <= pos[0] < self.height and 0 <= pos[1] < self.width):
            raise IndexError("Row or column index out of bounds")
        
        return self.grid[pos[0]][pos[1]]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the entire grid on the given screen.
        
        :param screen: The screen on which to draw the grid.
        :type screen: pygame.Surface
        """
        
        for row in self.grid:
            for square in row:
                square.draw(screen, self.customizable_cost)

    def get_start(self) -> Square:
        """
        Returns the position of the start square as a tuple (row, col) or None if not found.
        
        :return: The square representing the start position, or None if not found.
        :rtype: Square or None
        """
        
        for row in self.grid:
            for square in row:
                if square.state.is_start():
                    return square
        return None
    
    def get_goal(self) -> Square:
        """
        Returns the position of the goal square as a tuple (row, col) or None if not found.

        :return: The square representing the goal position, or None if not found.
        :rtype: Square or None
        """

        for row in self.grid:
            for square in row:
                if square.state.is_goal():
                    return square
                
        return None

    def change_state(self, row: int, col: int, new_state: State) -> None:
        """
        Changes the state of the square at the specified row and column.

        :param row: The row index of the square.
        :type row: int
        :param col: The column index of the square.
        :type col: int
        :param new_state: The new state to set for the square.
        :type new_state: State

        :raises ValueError: If new_state is not an instance of State Enum.
        :raises IndexError: If the row or column index is out of bounds.
        """
        
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of State Enum")

        if not (0 <= row < self.height and 0 <= col < self.width):
            raise IndexError("Row or column index out of bounds")

        target_square = self.grid[row][col]
        
        match new_state:
            case State.START:
                self._clear_existing_start()
                target_square.change_state(new_state)
                
            case State.GOAL:
                self._clear_existing_goal()
                target_square.change_state(new_state)
                
            case State.ACTIVATED:
                if not target_square.state.is_start():
                    target_square.change_state(new_state)
                    
            case _:
                target_square.change_state(new_state)

    def _clear_existing_start(self) -> None:
        """ Clears any existing START square. """
        current_start = self.get_start()
        if current_start:
            current_start.change_state(State.ACTIVATED)

    def _clear_existing_goal(self) -> None:
        """ Clears any existing GOAL square. """
        current_goal = self.get_goal()
        if current_goal:
            current_goal.change_state(State.ACTIVATED)

    def get_neighbors(self, square: Square) -> Iterator[Square]:
        """
        Returns the valid neighbors of a given square in the grid.
        This method yields the coordinates of the neighboring squares
        that are within the bounds of the grid.

        :param square: The square for which to find neighbors.
        :type square: Square

        :return: A list of neighboring squares.
        :rtype: Iterator[Square]
        """

        for d_row, d_col in [(-1,0),(1,0),(0,-1),(0,1)]:
            n_row, n_col = square.row + d_row, square.col + d_col
            if 0 <= n_row < self.height and 0 <= n_col < self.width:
                yield self.grid[n_row][n_col]

    def get_moving_cost(self, node: Square,neighbor: Square) -> int:
        """
        Returns the cost of moving from one square to its neighbor.
        
        :param node: The current square.
        :type node: Square
        :param neighbor: The neighboring square.
        :type neighbor: Square

        :return: The cost of moving to the neighbor square.
        :rtype: int
        """
        
        return neighbor.cost


def manhattan_heuristic(node: Square, goal: Square) -> int:
    """ 
    Calculates the Manhattan distance heuristic between two squares.
    
    :param node: The current square.
    :type node: Square
    :param goal: The goal square.
    :type goal: Square
    
    :return: The Manhattan distance between the node and the goal.
    :rtype: int
    """
    
    return abs(node.row - goal.row) + abs(node.col - goal.col)
