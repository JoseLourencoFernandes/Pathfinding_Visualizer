import pygame
from definitions import Color, SquareState, SQUARE_SIZE, SPACING


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
        
    Methods:
        draw(screen): Draws the square on the given screen based on its state.
        change_state(new_state): Changes the state of the square to a new state.
    """
    def __init__(self, x, y, size, state):
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        
    def draw(self, screen):
        """
        Draws the square on the given screen based on its state.
        
        Arguments:
            screen: The screen on which to draw the square.
        """
        if (self.state.is_activated()):
            pygame.draw.rect(screen, Color.GRAY, (self.x, self.y, self.size, self.size))
        elif (self.state.is_start()):
            pygame.draw.rect(screen, Color.GREEN, (self.x, self.y, self.size, self.size))
        elif (self.state.is_goal()):
            pygame.draw.rect(screen, Color.RED, (self.x, self.y, self.size, self.size))
        elif (self.state == SquareState.DEACTIVATED):
            pygame.draw.rect(screen, Color.BROWN, (self.x, self.y, self.size, self.size))
        elif (self.state == SquareState.VISITED):
            pygame.draw.rect(screen, Color.PALEGREEN, (self.x, self.y, self.size, self.size))
        elif (self.state == SquareState.PATH):
            pygame.draw.rect(screen, Color.LIGHTBLUE, (self.x, self.y, self.size, self.size))
        elif (self.state == SquareState.FRONTIER):
            pygame.draw.rect(screen, Color.ORANGE, (self.x, self.y, self.size, self.size))
    
    def change_state(self, new_state):
        """
        Changes the state of the square to a new state.
        
        Arguments:
            new_state (State): The new state to set for the square.
        
        Raises:
            ValueError: If new_state is not an instance of State Enum.
        """
        if not isinstance(new_state, SquareState):
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
    def __init__(self, width, height, square_size=SQUARE_SIZE, spacing=SPACING, state=SquareState.ACTIVATED):
        self.width = width
        self.height = height
        self.grid = []
        for row in range(height):
            row_list = []
            for col in range(width):
                x = spacing + col * (square_size + spacing)
                y = spacing + row * (square_size + spacing)
                row_list.append(Square(x, y, square_size, state))
            self.grid.append(row_list)
    
    def get(self, row, col):
        """
        Returns the square at the specified row and column.
        
        Arguments:
            row (int): The row index of the square.
            col (int): The column index of the square.
            
        Returns:
            Square: The square at the specified row and column.
            
        Raises:
            IndexError: If the row or column index is out of bounds.
        """
        if not (0 <= row < self.height and 0 <= col < self.width):
            raise IndexError("Row or column index out of bounds")
        return self.grid[row][col]

    def draw(self, screen):
        """
        Draws the entire grid on the given screen.
        
        Arguments:
            screen: The screen on which to draw the grid.
        """
        for row in self.grid:
            for square in row:
                square.draw(screen)

    def get_start(self):
        """
        Returns the position of the start square as a tuple (row, col) or None if not found.
        
        Returns:
            tuple: A tuple (row, col) representing the position of the start square, or None if not found.
        """
        for row in self.grid:
            for square in row:
                if square.state.is_start():
                    return (self.grid.index(row), row.index(square))
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
                    return (self.grid.index(row), row.index(square))
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
        if not isinstance(new_state, SquareState):
            raise ValueError("new_state must be an instance of State Enum")
        
        # Validate row and col indices
        if not (0 <= row < self.height and 0 <= col < self.width):
            return 

        # Change the state of the square at (row, col)
        if new_state.is_start():
            start_pos = self.get_start()
            if start_pos is not None:
                self.grid[start_pos[0]][start_pos[1]].change_state(SquareState.ACTIVATED)
            self.grid[row][col].change_state(SquareState.START)
        elif new_state.is_goal():
            goal_pos = self.get_goal()
            if goal_pos is not None:
                self.grid[goal_pos[0]][goal_pos[1]].change_state(SquareState.ACTIVATED)
            self.grid[row][col].change_state(SquareState.GOAL)
        elif new_state.is_activated():
            if self.grid[row][col].state.is_start():
                self.grid[row][col].change_state(SquareState.ACTIVATED)
            else:
                self.grid[row][col].change_state(new_state)
        else:
            self.grid[row][col].change_state(new_state)