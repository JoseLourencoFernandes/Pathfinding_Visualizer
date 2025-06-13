# Import necessary libraries and modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import math
import copy
import time
from definitions import State, Color, SQUARE_SIZE, SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING, TIME_TEXT_X, TIME_TEXT_Y
from algorithms import BFSAlgorithm, DFSAlgorithm, DijkstraAlgorithm, AStarAlgorithm, GreedyBestFirstAlgorithm, generate_maze_prim
from classes.grid import Grid
from classes.button import Button
from appstate import AppState

# Function responsible for drawing all elements on the screen
def draw():
    # Draw the screen
    screen.fill(Color.BLACK)
    
    # Draw grid
    for row in range(grid.height):
        for col in range(grid.width):
            square = grid.get(row, col)
            square.draw(screen)
    
    # Draw execution time text
    time_text = font.render(f"Execution Time: {state.execution_time:.4f} s", True, Color.WHITE)
    screen.blit(time_text, (TIME_TEXT_X, TIME_TEXT_Y))
        
    # Draw buttons
    for idx, button in enumerate(buttons):
        if idx == 0:
            button.draw(screen, font, active=state.set_start_mode)
        elif idx == 1:
            button.draw(screen, font, active=state.set_goal_mode)
        elif idx >= 2 and idx <= 8:
            button.draw(screen, font, active=state.running_algorithm)  
            

# Main function to run the pygame application
if __name__ == '__main__':
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
    print(size)
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
        Button(BUTTON_X, BUTTON_Y + 8*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Maze (Prim)", Color.LIGHTBLUE)
    ]
    
    # Initialize the application state
    state = AppState() 
    
    # Set initial state of the grid
    running = True
    algorithm = None
    initial_grid_state = [[square.state for square in row] for row in grid.grid]  # Store initial state of the grid   

    # Main loops
    while running:
        
        # Get the mouse position and check if it's within the grid
        mouse_pos = pygame.mouse.get_pos()
        pos_x = math.floor(mouse_pos[0] / (SQUARE_SIZE + SPACING))
        pos_y = math.floor(mouse_pos[1] / (SQUARE_SIZE + SPACING))
        in_grid = (0 <= pos_x < grid.width) and (0 <= pos_y < grid.height)
        over_button = any(button.rect.collidepoint(mouse_pos) for button in buttons)
        
        # poll for events
        for event in pygame.event.get():
            # check for quit event or key press
            if event.type == pygame.QUIT :
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    running = False
                
            # check for mouse motion events
            if not state.running_algorithm:
                # check the mouse button down event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the left mouse button is pressed and the mouse is over the grid
                    if event.button == 1 and in_grid and not over_button:
                        if state.set_start_mode:
                            grid.change_state(pos_y, pos_x, State.START)
                            state.set_start_mode = False
                            state.set_goal_mode = False
                            state.ignore_drag = True
                        elif state.set_goal_mode:
                            grid.change_state(pos_y, pos_x, State.GOAL)
                            state.set_goal_mode = False
                            state.set_start_mode = False
                            state.ignore_drag = True

                    # If the button is pressed
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(mouse_pos):
                            if idx == 0:
                                state.set_start_mode = True
                                state.set_goal_mode = False
                            elif idx == 1:
                                state.set_goal_mode = True
                                state.set_start_mode = False
                            elif idx == 7:  # Reset button
                                state.runned_algorithm = False   
                                if state.grid_state == 1:
                                    for row in range(grid.height):
                                        for col in range(grid.width):
                                            grid.grid[row][col].change_state(initial_grid_state[row][col])
                                    state.execution_time = 0.0
                                    state.grid_state = 0
                                else:
                                    for row in range(grid.height):
                                        for col in range(grid.width):
                                            grid.grid[row][col].change_state(State.ACTIVATED)
                            elif idx == 8:  # Maze (Prim) button
                                    generate_maze_prim(grid)
                            else:
                                if grid.get_start() is None or grid.get_goal() is None or state.runned_algorithm:
                                    continue
                                if not state.runned_algorithm:
                                    initial_grid_state = copy.deepcopy([[square.state for square in row] for row in grid.grid])
                                state.runned_algorithm = True
                                state.grid_state = 1
                                state.start_time = time.time()
                                state.running_algorithm = True
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
                                    
                    # check for mouse button release
                elif event.type == pygame.MOUSEBUTTONUP:
                    state.ignore_drag = False

        # check if the user has requested to quit
        if not running:
            break
    
        # If the algorithm is running, step through it
        if state.running_algorithm and algorithm is not None:
            state.execution_time = time.time() - state.start_time  # Update execution time
            if not algorithm.step():
                state.running_algorithm = False
                algorithm.highlight_path()  # Highlight the path after BFS completes

        if not state.running_algorithm:
            # Get mouse state
            mouse_state = pygame.mouse.get_pressed()
            # Handle mouse dragging
            if in_grid and not over_button and mouse_state[0] and not state.ignore_drag:
                grid.change_state(pos_y, pos_x, State.DEACTIVATED)
            elif in_grid and not over_button and mouse_state[2] and not state.ignore_drag:
                grid.change_state(pos_y, pos_x, State.ACTIVATED)
        
        # Draw the current state of the elements
        draw() 
            
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()