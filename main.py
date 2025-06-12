# Example file showing a basic pygame "game loop"
import pygame
from enum import Enum
import math
import time

# Screen Constants
SPACING = 5
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 705

# Button Constants
BUTTON_WIDTH = 450
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
BUTTON_X = SCREEN_WIDTH - BUTTON_WIDTH - (SCREEN_WIDTH - BUTTON_WIDTH - SCREEN_HEIGHT) / 2 
BUTTON_Y = 50

# Square Constants
SQUARE_SIZE = 20

# Color Constants
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (102, 205, 0)
    RED = (181, 42, 42)
    GRAY = (50, 50, 50)
    BROWN = (205, 170, 125)
    LIGHTGREEN = (144, 238, 144)
    TOMATO = (255, 99, 71)
    
# State Enum to represent the state of each square
class State(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    START = 2
    GOAL = 3
    
    def is_activated(self):
        return self == State.ACTIVATED
    
    def is_start(self):
        return self == State.START
    
    def is_goal(self):
        return self == State.GOAL
    
# Button class
class Button:
    def __init__(self, x, y, w, h, text, color= Color.GRAY, text_color= Color.BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface, font, active = False):
        if active:
            color = (min(self.color[0]+100,255), min(self.color[1]+100,255), min(self.color[2]+100,255))
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
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
    
    def change_state(self, new_state):
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of State Enum")

        self.state = new_state

# Matrix class to represent the grid of squares
class Matrix:
    def __init__(self, width, height, square_size=SQUARE_SIZE, spacing=SPACING, state=State.ACTIVATED):
        self.width = width
        self.height = height
        self.matrix = []
        for row in range(height):
            row_list = []
            for col in range(width):
                x = spacing + col * (square_size + spacing)
                y = spacing + row * (square_size + spacing)
                row_list.append(Square(x, y, square_size, state))
            self.matrix.append(row_list)
    
    def get(self, row, col):
        return self.matrix[row][col]

    def draw(self, surface):
        for row in self.matrix:
            for square in row:
                square.draw(surface)

    def exists_start(self):
        for row in self.matrix:
            for square in row:
                if square.state.is_start():
                    return (self.matrix.index(row), row.index(square))
        return None
    
    def exists_goal(self):
        for row in self.matrix:
            for square in row:
                if square.state.is_goal():
                    return (self.matrix.index(row), row.index(square))
        return None

    def change_state(self, row, col, new_state):
        if not (0 <= row < self.height and 0 <= col < self.width):
            return  # Ignore invalid indices

        if new_state.is_start():
            start_pos = self.exists_start()
            if start_pos is not None:
                self.matrix[start_pos[0]][start_pos[1]].change_state(State.ACTIVATED)
            self.matrix[row][col].change_state(State.START)
        elif new_state.is_goal():
            goal_pos = self.exists_goal()
            if goal_pos is not None:
                self.matrix[goal_pos[0]][goal_pos[1]].change_state(State.ACTIVATED)
            self.matrix[row][col].change_state(State.GOAL)
        elif new_state.is_activated():
            if self.matrix[row][col].state.is_start():
                self.matrix[row][col].change_state(State.ACTIVATED)
            else:
                self.matrix[row][col].change_state(new_state)
        else:
            self.matrix[row][col].change_state(new_state)






# Main function to run the pygame application
if __name__ == '__main__':
    # Initialize pygame and create a window 
    pygame.init()
    pygame.display.set_caption("Searchin Algorithms Visualizer")
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(Color.BLACK)

    # Set up the clock for a decent framerate
    clock = pygame.time.Clock()

    # Set up the font for rendering text
    font = pygame.font.SysFont(None, 32)
    
    # Initialize squares objects
    size = SCREEN_HEIGHT // (SQUARE_SIZE + SPACING)
    matrix = Matrix(size, size, SQUARE_SIZE, SPACING)

    # Create buttons
    buttons = [
        Button(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Set Start", Color.LIGHTGREEN),
        Button(BUTTON_X, BUTTON_Y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Set Goal", Color.TOMATO),
        Button(BUTTON_X, BUTTON_Y + 2*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Algorithm 1"),
        Button(BUTTON_X, BUTTON_Y + 3*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Algorithm 2"),
        Button(BUTTON_X, BUTTON_Y + 4*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Algorithm 3"),
        Button(BUTTON_X, BUTTON_Y + 5*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Algorithm 4"),
    ]

    # Initialize variables
    running = True
    set_start_mode = False
    set_goal_mode = False
    ignore_drag = False

    # Main loops
    while running:
        
        # Get the mouse position and check if it's within the grid
        mouse_pos = pygame.mouse.get_pos()
        pos_x = math.floor(mouse_pos[0] / (SQUARE_SIZE + SPACING))
        pos_y = math.floor(mouse_pos[1] / (SQUARE_SIZE + SPACING))
        in_grid = (0 <= pos_x < matrix.width) and (0 <= pos_y < matrix.height)
        over_button = any(button.rect.collidepoint(mouse_pos) for button in buttons)
        
        # poll for events
        for event in pygame.event.get():
            # check for quit event or key press
            if event.type == pygame.QUIT or (event.type == pygame.K_LCTRL and event.type == pygame.K_z):
                running = False
                break
            # check the mouse button down event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button is pressed and the mouse is over the grid
                if event.button == 1 and in_grid and not over_button:
                    if set_start_mode:
                        matrix.change_state(pos_y, pos_x, State.START)
                        set_start_mode = False
                        set_goal_mode = False
                        ignore_drag = True
                    elif set_goal_mode:
                        matrix.change_state(pos_y, pos_x, State.GOAL)
                        set_goal_mode = False
                        set_start_mode = False
                        ignore_drag = True
                
                # If the button is pressed
                for idx, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        if idx == 0:
                            set_start_mode = True
                            set_goal_mode = False
                        elif idx == 1:
                            set_goal_mode = True
                            set_start_mode = False
                        elif idx == 2:
                            print("Algorithm 1 button clicked")
                        elif idx == 3:
                            print("Algorithm 2 button clicked")
                        elif idx == 4:
                            print("Algorithm 3 button clicked")
                        elif idx == 5:
                            print("Algorithm 4 button clicked")
            # check for mouse button release
            elif event.type == pygame.MOUSEBUTTONUP:
                ignore_drag = False

        # check if the user has requested to quit
        if not running:
            break
        
        # Get mouse state
        mouse_state = pygame.mouse.get_pressed()
        # Handle mouse dragging
        if in_grid and not over_button and mouse_state[0] and not ignore_drag:
            matrix.change_state(pos_y, pos_x, State.DEACTIVATED)
        elif in_grid and not over_button and mouse_state[2] and not ignore_drag:
            matrix.change_state(pos_y, pos_x, State.ACTIVATED)    
        
        # Draw grid
        for row in range(matrix.height):
            for col in range(matrix.width):
                square = matrix.get(row, col)
                square.draw(screen)
        
        # Draw buttons
        for idx, button in enumerate(buttons):
            if idx == 0:
                button.draw(screen, font, active=set_start_mode)
            elif idx == 1:
                button.draw(screen, font, active=set_goal_mode)
            else:
                button.draw(screen, font)
            
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()