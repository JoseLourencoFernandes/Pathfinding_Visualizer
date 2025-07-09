# Import necessary libraries and modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from definitions.global_constants import Screen, SCREEN_WIDTH, SCREEN_HEIGHT
from app_state import GlobalAppState
from screens.main_menu import MainMenuScreen
from screens.grid_2d import Grid2DScreen
from screens.grid_2d import Grid2DWeightedScreen
from screens.graph_screen import GraphScreen

def main():
    """
    Main function to initialize the Pygame application and run the main loop.
    This function sets up the Pygame environment, initializes the global application state,
    creates the main window, and manages the event loop for the application.
    It handles user input, updates the current screen based on user actions, and draws the appropriate content.
    The main loop continues until the user decides to quit the application.
    """""
    
    # Initialize the global application state
    app_state = GlobalAppState()

    # Initialize Pygame and create the main window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")

    # Define the screens and their corresponding classes
    screens = {
        Screen.MAIN_MENU: MainMenuScreen(screen, app_state),
        Screen.GRID_2D: Grid2DScreen(screen, app_state),
        Screen.GRID_2D_WEIGHTED: Grid2DWeightedScreen(screen, app_state),
        Screen.GRAPH: GraphScreen(screen, app_state)
    }
    
    # Define the previous screen to track the last active screen
    previous_screen = app_state.current_screen

    # Set up the clock for a decent framerate
    clock = pygame.time.Clock()

    # Set the running flag to True to start the main loop
    running = True
    
    # Run the main loop
    while running:
        # Process events
        for event in pygame.event.get():
            # Check for quit event
            if event.type == pygame.QUIT:
                running = False
                
            # Check for keydown event to quit with Ctrl+Q
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    running = False
                    
            # Handle events for the currently active screen
            screens[app_state.current_screen].handle_event(event)
            
            # Handle screen transitions and ignore drag state
            if app_state.current_screen != previous_screen:
                if app_state.current_screen in (Screen.GRID_2D, Screen.GRID_2D_WEIGHTED, Screen.GRAPH):
                    screens[app_state.current_screen].local_app_state.ignore_drag = True
                previous_screen = app_state.current_screen
        
        # If user as requested to quit, exit the loop
        if not running:
            break
        
        # Run the logic for the currently active screen
        screens[app_state.current_screen].run()
        
        # Draw the currently active screen
        screens[app_state.current_screen].draw()
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    # Quit Pygame when the main loop ends
    pygame.quit()

# This is the main entry point of the application.
if __name__ == "__main__":
    main()