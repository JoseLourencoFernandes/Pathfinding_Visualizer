# Import necessary libraries and modules
import pygame
import math
import copy
from definitions import State, Color, SQUARE_SIZE, SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING
from algorithms import BFSAlgorithm, DFSAlgorithm, DijkstraAlgorithm, AStarAlgorithm
from classes import Square, Grid, Button

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
    grid = Grid(size, size, SQUARE_SIZE, SPACING)

    # Create buttons
    buttons = [
        Button(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Set Start", Color.LIGHTGREEN),
        Button(BUTTON_X, BUTTON_Y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Set Goal", Color.TOMATO),
        Button(BUTTON_X, BUTTON_Y + 2*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "BFS Algorithm"),
        Button(BUTTON_X, BUTTON_Y + 3*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "DFS Algorithm"),
        Button(BUTTON_X, BUTTON_Y + 4*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Dijkstra Algorithm"),
        Button(BUTTON_X, BUTTON_Y + 5*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "A* Algorithm"),
        Button(BUTTON_X, BUTTON_Y + 6*(BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT, "Reset", Color.GRAY)
    ]

    # Initialize variables
    running = True
    set_start_mode = False
    set_goal_mode = False
    ignore_drag = False
    
    algorithm = None
    running_algorithm = False
    initial_grid_state = [[square.state for square in row] for row in grid.grid]  # Store initial state of the grid
    grid_state = 0

    # Main loops
    while running:
        
        # Get the mouse position and check if it's within the grid
        mouse_pos = pygame.mouse.get_pos()
        pos_x = math.floor(mouse_pos[0] / (SQUARE_SIZE + SPACING))
        pos_y = math.floor(mouse_pos[1] / (SQUARE_SIZE + SPACING))
        in_grid = (0 <= pos_x < grid.width) and (0 <= pos_y < grid.height)
        over_button = any(button.rect.collidepoint(mouse_pos) for button in buttons)
        
        # poll for events
        if not running_algorithm:
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
                            grid.change_state(pos_y, pos_x, State.START)
                            set_start_mode = False
                            set_goal_mode = False
                            ignore_drag = True
                        elif set_goal_mode:
                            grid.change_state(pos_y, pos_x, State.GOAL)
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
                            elif idx == 6:  # Reset button     
                                if grid_state == 1:
                                    for row in range(grid.height):
                                        for col in range(grid.width):
                                            grid.grid[row][col].change_state(initial_grid_state[row][col])
                                    grid_state = 0
                                else:
                                    for row in range(grid.height):
                                        for col in range(grid.width):
                                            grid.grid[row][col].change_state(State.ACTIVATED)
                
                            else:
                                if grid.get_start() is None or grid.get_goal() is None:
                                    continue
                                initial_grid_state = copy.deepcopy([[square.state for square in row] for row in grid.grid])
                                grid_state = 1
                                running_algorithm = True
                                if idx == 2:
                                    algorithm = BFSAlgorithm(grid)
                                elif idx == 3:
                                    algorithm = DFSAlgorithm(grid)
                                elif idx == 4:
                                    algorithm = DijkstraAlgorithm(grid)
                                elif idx == 5:
                                    algorithm = AStarAlgorithm(grid)
                    # check for mouse button release
                elif event.type == pygame.MOUSEBUTTONUP:
                    ignore_drag = False

        # check if the user has requested to quit
        if not running:
            break
        
        # If the BFS algorithm is running, step through it
        if running_algorithm and algorithm is not None:
            if not algorithm.step():
                running_algorithm = False
                algorithm.highlight_path()  # Highlight the path after BFS completes

        if not running_algorithm:
            # Get mouse state
            mouse_state = pygame.mouse.get_pressed()
            # Handle mouse dragging
            if in_grid and not over_button and mouse_state[0] and not ignore_drag:
                grid.change_state(pos_y, pos_x, State.DEACTIVATED)
            elif in_grid and not over_button and mouse_state[2] and not ignore_drag:
                grid.change_state(pos_y, pos_x, State.ACTIVATED)    
        
        # Draw grid
        for row in range(grid.height):
            for col in range(grid.width):
                square = grid.get(row, col)
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