# Import necessary libraries and modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import math
import copy
import time
from definitions import SquareState, Color, SQUARE_SIZE, SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING, TIME_TEXT_X, TIME_TEXT_Y
from algorithms import BFSAlgorithm, DFSAlgorithm, DijkstraAlgorithm, AStarAlgorithm, GreedyBestFirstAlgorithm, generate_maze_prim
from classes.grid import Grid
from classes.button import Button
from appstate import AppState


def get_mouse_position():
    """
    Get the current mouse position and check if it is within the grid.
    This function calculates the position of the mouse in terms of grid coordinates
    and checks if the mouse is over any of the buttons.
    
    Returns:
        mouse_pos (tuple): The current mouse position (x, y).
        pos_x (int): The x-coordinate of the mouse in grid terms.
        pos_y (int): The y-coordinate of the mouse in grid terms.
        in_grid (bool): True if the mouse is within the grid, False otherwise.
        over_button (bool): True if the mouse is over any button, False otherwise.
    """
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / (SQUARE_SIZE + SPACING))
    pos_y = math.floor(mouse_pos[1] / (SQUARE_SIZE + SPACING))
    in_grid = (0 <= pos_x < grid.width) and (0 <= pos_y < grid.height)
    over_button = any(button.rect.collidepoint(mouse_pos) for button in buttons)
    
    return mouse_pos, pos_x, pos_y, in_grid, over_button



def set_button_mode(pos_x, pos_y, state_enum):
    """
    Set the state of a square in the grid to a specific state.
    This function changes the state of a square in the grid based on the mouse position
    and the specified state enum. It also updates the application state to reflect
    that the user is no longer in set mode for start or goal.
    
    Arguments:
        pos_x (int): The x-coordinate of the square in grid terms.
        pos_y (int): The y-coordinate of the square in grid terms.
        state_enum (State): The state to set for the square (START or GOAL).
    """   
    global grid, app_state
    grid.change_state(pos_y, pos_x, state_enum)
    app_state.set_goal_mode = False
    app_state.set_start_mode = False
    app_state.ignore_drag = True
    
def reset_button():
    """
    Reset the grid to its latest relevant state.
    This function resets the grid to the state it was in before the last algorithm was run
    or fully resets it if no algorithm has been run yet. It also updates the application state
    to indicate that no algorithm is currently running and that the grid has been fully reset.
    """
    
    app_state.runned_algorithm = False
    
    # Restore grid
    if app_state.grid_full_reset == False:
        for row in range(grid.height):
            for col in range(grid.width):
                grid.get(row, col).change_state(grid_reset_state[row][col])
        app_state.grid_full_reset = True
    else:
        for row in range(grid.height):
            for col in range(grid.width):
                grid.get(row, col).change_state(SquareState.ACTIVATED)


def process_events():
    """
    Process user input events.
    This function handles mouse clicks, key presses, and mouse motion events.
    """
    global running, algorithm, grid_reset_state
    
    # Get the mouse position and check if it's within the grid
    mouse_pos, pos_x, pos_y, in_grid, over_button = get_mouse_position()
    
    # poll for events
    for event in pygame.event.get():
        # check if the user has requested to quit
        if event.type == pygame.QUIT :
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check for key presses to quit or reset the grid
            if event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                running = False
            elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL) and not app_state.running_algorithm:
                reset_button()
            
        # check the mouse button down event if the algorithm is not running
        if event.type == pygame.MOUSEBUTTONDOWN and not app_state.running_algorithm:
            
            # If the left mouse button is pressed and the mouse is over the grid
            if event.button == 1 and in_grid and not over_button:
                if app_state.set_start_mode:
                    set_button_mode(pos_x, pos_y, SquareState.START)
                elif app_state.set_goal_mode:
                    set_button_mode(pos_x, pos_y, SquareState.GOAL)

            # If the button is pressed
            for idx, button in enumerate(buttons):
                if button.is_clicked(mouse_pos):
                    handle_button_click(idx)
                            
        # check for mouse button release if the algorithm is not running
        elif event.type == pygame.MOUSEBUTTONUP and not app_state.running_algorithm:
            app_state.ignore_drag = False
        

def handle_button_click(idx):
    """
    Handle button click events based on the index of the button clicked.
    This function updates the application state and initializes the algorithms.
    
    Arguments:
        idx -- The index of the button clicked.
    """
    global algorithm, grid_reset_state
    
    # Deselect start and goal modes if any button is clicked
    app_state.set_start_mode = False
    app_state.set_goal_mode = False
    
    if idx == 0: # Activate start mode
        # If an algorithm has been runned before, reset the grid
        if app_state.runned_algorithm:
            reset_button()
        app_state.set_start_mode = True
        app_state.set_goal_mode = False
    elif idx == 1: # Activate goal mode
        # If an algorithm has been runned before, reset the grid
        if app_state.runned_algorithm:
            reset_button()
        app_state.set_goal_mode = True
        app_state.set_start_mode = False
    
    elif idx == 7: # Reset button
        reset_button()
    elif idx == 8:  # Maze (Prim) button
        reset_button()  # Reset the grid before generating a maze
        generate_maze_prim(grid)
    else: # Algorithm buttons
        # Manage the state of the application
        if grid.get_start() is None or grid.get_goal() is None:
            return
        
        if app_state.runned_algorithm:
            reset_button()  # Reset the grid if an algorithm has been runned before
        
        if not app_state.runned_algorithm: # If an algorithm is not runned yet
            grid_reset_state = copy.deepcopy([[square.state for square in row] for row in grid.grid])
        
        # Set the application state
        app_state.runned_algorithm = True
        app_state.grid_full_reset = False
        app_state.start_time = time.time()
        app_state.running_algorithm = True
        
        if idx == 2:
            algorithm = BFSAlgorithm(grid)
        elif idx == 3:
            algorithm = DFSAlgorithm(grid)
        elif idx == 4:
            algorithm = DijkstraAlgorithm(grid)
        elif idx == 5:
            algorithm = AStarAlgorithm(grid)
        elif idx == 6:
            algorithm = GreedyBestFirstAlgorithm(grid)
            
            
def update_algorithm():
    """
    Update the algorithm state and execution time.
    This function actualize the algorithm step and updates the execution time.
    If the algorithm completes, it highlights the final path calculated by the algorithm.
    """
    app_state.execution_time = time.time() - app_state.start_time  # Update execution time
    if not algorithm.step():
        app_state.running_algorithm = False
        algorithm.highlight_path()  # Highlight the path after BFS completes


def draw():
    """
    Draw the elements on the screen.
    This function draws the grid, buttons, and execution time text.
    """
    # Draw the screen
    screen.fill(Color.BLACK)
    
    # Draw grid
    for row in range(grid.height):
        for col in range(grid.width):
            square = grid.get(row, col)
            square.draw(screen)
    
    # Draw execution time text
    time_text = font.render(f"Execution Time: {app_state.execution_time:.4f} s", True, Color.WHITE)
    screen.blit(time_text, (TIME_TEXT_X, TIME_TEXT_Y))
        
    # Draw buttons
    for idx, button in enumerate(buttons):
        if idx == 0:
            button.draw(screen, font, active=app_state.set_start_mode or app_state.running_algorithm)
        elif idx == 1:
            button.draw(screen, font, active=app_state.set_goal_mode or app_state.running_algorithm)
        elif idx >= 2 and idx <= 8:
            button.draw(screen, font, active=app_state.running_algorithm)  


def handle_mouse_drag():
    """
    Handle mouse dragging events to change the state of squares in the grid.
    This function checks if the mouse is pressed and updates the state of the
    squares based on the mouse position and the current application state.
    """

    # Get the mouse position and check if it's within the grid
    _, pos_x, pos_y, in_grid, over_button = get_mouse_position()
    
    # Get the mouse state
    mouse_state = pygame.mouse.get_pressed()
    # Handle mouse dragging action
    if in_grid and not over_button and mouse_state[0] and not app_state.ignore_drag:
        # Reset the grid if an algorithm has been runned before
        if app_state.runned_algorithm:
            reset_button()  
        grid.change_state(pos_y, pos_x, SquareState.DEACTIVATED)
    elif in_grid and not over_button and mouse_state[2] and not app_state.ignore_drag:
        # Reset the grid if an algorithm has been runned before
        if app_state.runned_algorithm:
            reset_button()  
        grid.change_state(pos_y, pos_x, SquareState.ACTIVATED)


if __name__ == '__main__':
    """ 
    Main function to initialize the application and run the main loop.
    This function sets up the pygame environment, initializes the grid 
    and buttons, and runs the main event loop.
    """
    
    # Initialize pygame and create a window
    pygame.init()
    pygame.display.set_caption("Searching Algorithms Visualizer")
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(Color.BLACK)

    # Set up the clock for a decent framerate
    clock = pygame.time.Clock()

    # Set up the font for rendering text
    font = pygame.font.SysFont(None, 32)
    
    # Initialize squares objects
    size = SCREEN_HEIGHT // (SQUARE_SIZE + SPACING)

    # Initialize the grid with the specified size, square size, and spacing
    grid = Grid(size, size, SQUARE_SIZE, SPACING)

    # Create buttons
    buttons = [
        Button(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Set Start", Color.LIGHTGREEN),
        Button(BUTTON_X, BUTTON_Y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Set Goal", Color.TOMATO),
        Button(BUTTON_X, BUTTON_Y + 2*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "BFS Algorithm", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 3*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "DFS Algorithm", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 4*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Dijkstra Algorithm", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 5*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "A* Algorithm", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 6*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Greedy Best First Algorithm", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 7*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Reset", Color.TANGERINE),
        Button(BUTTON_X, BUTTON_Y + 8*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Generate Maze (Using Prim Algorithm)", Color.LIGHTBLUE)
    ]
    
    # Initialize the application state
    app_state = AppState() 

    # Initialize program flags
    running = True
    algorithm = None
    start_time = None
    grid_reset_state = []   

    # Main loops
    while running:
        process_events()
        # check if the user has requested to quit
        if not running:
            break
    
        # Update the algorithm step if an algorithm is running
        if app_state.running_algorithm:
            update_algorithm()
        
        # Handle mouse drag events if not running an algorithm
        if not app_state.running_algorithm:
            handle_mouse_drag()
        
        # Draw the current state of the elements
        draw() 
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()