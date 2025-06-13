import pygame
from definitions import Color, State, SQUARE_SIZE, SPACING

# Square class to represent each square in the grid
class Square:
    def __init__(self, x, y, size, state):
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        
    def draw(self, surface):
        if (self.state.is_activated()):
            pygame.draw.rect(surface, Color.GRAY, (self.x, self.y, self.size, self.size))
        elif (self.state.is_start()):
            pygame.draw.rect(surface, Color.GREEN, (self.x, self.y, self.size, self.size))
        elif (self.state.is_goal()):
            pygame.draw.rect(surface, Color.RED, (self.x, self.y, self.size, self.size))
        elif (self.state == State.DEACTIVATED):
            pygame.draw.rect(surface, Color.BROWN, (self.x, self.y, self.size, self.size))
        elif (self.state == State.VISITED):
            pygame.draw.rect(surface, Color.PALEGREEN, (self.x, self.y, self.size, self.size))
        elif (self.state == State.PATH):
            pygame.draw.rect(surface, Color.LIGHTBLUE, (self.x, self.y, self.size, self.size))
        elif (self.state == State.FRONTIER):
            pygame.draw.rect(surface, Color.ORANGE, (self.x, self.y, self.size, self.size))
    
    def change_state(self, new_state):
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of State Enum")

        self.state = new_state

# Grid class to represent the grid of squares
class Grid:
    def __init__(self, width, height, square_size=SQUARE_SIZE, spacing=SPACING, state=State.ACTIVATED):
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
        return self.grid[row][col]

    def draw(self, surface):
        for row in self.grid:
            for square in row:
                square.draw(surface)

    def get_start(self):
        for row in self.grid:
            for square in row:
                if square.state.is_start():
                    return (self.grid.index(row), row.index(square))
        return None
    
    def get_goal(self):
        for row in self.grid:
            for square in row:
                if square.state.is_goal():
                    return (self.grid.index(row), row.index(square))
        return None

    def change_state(self, row, col, new_state):
        if not (0 <= row < self.height and 0 <= col < self.width):
            return  # Ignore invalid indices

        if new_state.is_start():
            start_pos = self.get_start()
            if start_pos is not None:
                self.grid[start_pos[0]][start_pos[1]].change_state(State.ACTIVATED)
            self.grid[row][col].change_state(State.START)
        elif new_state.is_goal():
            goal_pos = self.get_goal()
            if goal_pos is not None:
                self.grid[goal_pos[0]][goal_pos[1]].change_state(State.ACTIVATED)
            self.grid[row][col].change_state(State.GOAL)
        elif new_state.is_activated():
            if self.grid[row][col].state.is_start():
                self.grid[row][col].change_state(State.ACTIVATED)
            else:
                self.grid[row][col].change_state(new_state)
        else:
            self.grid[row][col].change_state(new_state)