# Import necessary libraries and modules
import os
import sys
import pygame
import math
import copy
import time
from app_state import GlobalAppState
from definitions.global_constants import Screen, SCREEN_WIDTH, SCREEN_HEIGHT
from definitions.grid_constants import SQUARE_SIZE, SPACING, GRID_BUTTON_X, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, GRID_BUTTON_SPACING, TIME_TEXT_X, TIME_TEXT_Y
from definitions.colors import Color
from definitions.states import State
from algorithms import BFSAlgorithm, DFSAlgorithm, DijkstraAlgorithm, AStarAlgorithm, GreedyBestFirstAlgorithm, generate_maze_prim
from classes.grid import Grid
from classes.button import Button
from screens.screen_interface import ScreenInterface
from screens.button_panel_mixin import ButtonPanelMixin
from classes.grid import manhattan_heuristic

class BaseGridScreen(ScreenInterface, ButtonPanelMixin):
    """
    Base class for 2D grid screens.
    This class provides the basic functionality for handling a 2D grid, including
    initializing the grid, handling events, running algorithms, and drawing the grid and buttons.
    It is designed to be extended by specific grid screens, such as Grid2DScreen and Grid2DWeightedScreen.
    
    :param screen: The Pygame surface where the grid is drawn.
    :type screen: pygame.Surface
    :param app_state: The global application state that holds the current state of the app.
    :type app_state: GlobalAppState
    :param local_app_state: The local application state for the grid, which can be either Grid2DAppState or Grid2DWeightedAppState.
    :type local_app_state: Grid2DAppState | Grid2DWeightedAppState
    :param customizable_cost: Flag to indicate if the grid allows customizable costs (default is False).
    :type customizable_cost: bool
    :param font: The font used for rendering text on the screen (default is None, which uses the default Pygame font).
    :type font: pygame.font.Font | None
    :param square_size: The size of each square in the grid (default is SQUARE_SIZE).
    :type square_size: int
    :param spacing: The spacing between squares in the grid (default is SPACING).
    :type spacing: int
    :param grid: The grid object that holds the squares and their states.
    :type grid: Grid
    :param buttons: List of buttons for user interaction (default is an empty list).
    :type buttons: list[Button]
    :param back_button: Button to go back to the main menu (default is None).
    :type back_button: Button | None
    :param arrow_img: Image for the back button (default is None).
    :type arrow_img: pygame.Surface | None
    :param algorithm: The algorithm currently being run on the grid (default is None).
    :type algorithm: Algorithm | None
    :param start_time: The time when the algorithm started running (default is None).
    :type start_time: float | None
    :param grid_reset_state: The state of the grid before the last algorithm was run (default is an empty list).
    :type grid_reset_state: list[list[State]]

    This class is not meant to be instantiated directly, but rather serves as a base for other grid screens.
    """
    def __init__(self, screen: pygame.Surface, app_state: GlobalAppState, size: int, customizable_cost: bool = False, square_size: int = SQUARE_SIZE, spacing: int = SPACING, draw_centering_offset: int = 0) -> None:
        """ Constructor for the BaseGridScreen class. """
        super().__init__(screen, app_state)
        
        # Initialize the local application state based on whether the grid is customizable or not
        self.local_app_state = app_state.grid2d_app_state if not customizable_cost else app_state.grid2d_weighted_app_state
        
        # Set up the font for rendering text
        self.font = pygame.font.SysFont(None, 32)
        
        # Store the customizable square size, and spacing
        self.square_size = square_size
        self.spacing = spacing
        
        # Initialize the grid with the specified size, square size, and spacing
        # If try fails, print an error message and exit the program
        try:
            self.grid = Grid(size, size, square_size, spacing, customizable_cost=customizable_cost, offset=draw_centering_offset)
        except ValueError as e:
            print(f"Error initializing grid: {e}")
            sys.exit(1)

        # Create buttons
        self.buttons = self.create_default_buttons(object="Square", include_maze_button=True)
        
        # Load the arrow image for the back button
        arrow_path = os.path.join("assets", "arrow_left.png")
        self.arrow_img = pygame.image.load(arrow_path).convert_alpha()
        self.arrow_img = pygame.transform.smoothscale(self.arrow_img, (30, 30))

        # Back button to return to the main menu
        self.back_button = Button(pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40), color=Color.LIGHTBLUE, icon=self.arrow_img)

        # Initialize program flags
        self.algorithm = None
        self.start_time = None
        self.grid_reset_state = []


    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle user input events.
        This function processes mouse clicks, key presses, and mouse motion events.
        It updates the application state based on user interactions, such as clicking buttons
        or setting start and goal squares in the grid.
        
        :param event: The Pygame event to handle.
        :type event: pygame.event.Event
        """     
        # Block all mouse clicks until user releases mouse button after entering screen
        if self.local_app_state.block_action:
            if event.type == pygame.MOUSEBUTTONUP:
                self.local_app_state.block_action = False
            return
        
        # Get the mouse position and check if it's within the grid
        mouse_pos, pos_x, pos_y, in_grid, over_button = self._get_mouse_position()

        # Check if user has request to go back to the main menu
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_clicked(mouse_pos):
                self.app_state.current_screen = Screen.MAIN_MENU
                return  # Exit the event handling if back button is clicked

        elif event.type == pygame.KEYDOWN:
            # Check for key presses to quit or reset the grid
            # If the Escape key is pressed, go back to the main menu
            if event.key == pygame.K_ESCAPE:
                self.app_state.current_screen = Screen.MAIN_MENU
            # If Ctrl+Q is pressed, quit the application
            elif event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.local_app_state.running = False
            # If Ctrl+R is pressed and the algorithm is not running, reset the grid
            elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL) and not self.local_app_state.running_algorithm:
                self._reset_button()
            
        # Check the mouse button down event if the algorithm is not running
        if event.type == pygame.MOUSEBUTTONDOWN and not self.local_app_state.running_algorithm:
            # If the left mouse button is pressed and the mouse is over the grid set start or goal square
            if event.button == 1 and in_grid and not over_button:
                if self.local_app_state.set_start_mode:
                    self._set_button_mode(pos_x, pos_y, State.START)
                elif self.local_app_state.set_goal_mode:
                    self._set_button_mode(pos_x, pos_y, State.GOAL)

            # If the button is pressed and the mouse is over a button, handle the button click
            for idx, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos):
                    self.handle_button_click(idx)

        # Ensure that when entering the grid2d screen, the block_action flag is set to False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.local_app_state.block_action = False 
            
        # Check for mouse button release if the algorithm is not running
        elif event.type == pygame.MOUSEBUTTONUP and not self.local_app_state.running_algorithm:
            self.local_app_state.block_action = False


    def run(self) -> None:
        """
        Run the screen logic.
        This function updates the algorithm step if an algorithm is running,
        and handles mouse drag events if the algorithm is not running.
        """
        # Update the algorithm step if an algorithm is running
        if self.local_app_state.running_algorithm:
            self.update_algorithm()
        
        # Handle mouse drag events if not running an algorithm
        if not self.local_app_state.running_algorithm:
            self.handle_mouse_drag()


    def draw(self) -> None:
        """
        Draw the elements on the screen.
        This function draws the grid, buttons, and execution time text.
        It fills the screen with a background color and renders the grid and buttons.
        It also displays the execution time of the algorithm if it is running.
        """
        # Draw the screen
        self.screen.fill(Color.BLACK)
        
        # Draw grid
        self.grid.draw(self.screen)
        
        # Draw execution time text
        time_text = self.font.render(f"Execution Time: {self.local_app_state.execution_time:.4f} s", True, Color.WHITE)
        self.screen.blit(time_text, (TIME_TEXT_X, TIME_TEXT_Y))
        
        # Draw back button
        self.back_button.draw(self.screen, self.font)
            
        # Draw buttons
        for idx, button in enumerate(self.buttons):
            if idx == 0:
                button.draw(self.screen, self.font, active=self.local_app_state.set_start_mode or self.local_app_state.running_algorithm)
            elif idx == 1:
                button.draw(self.screen, self.font, active=self.local_app_state.set_goal_mode or self.local_app_state.running_algorithm)
            elif idx >= 2 and idx <= 8:
                button.draw(self.screen, self.font, active=self.local_app_state.running_algorithm)


    def _get_mouse_position(self) -> tuple[tuple, int, int, bool, bool]:
        """
        Get the current mouse position and check if it is within the grid.
        This function calculates the position of the mouse in terms of grid coordinates
        and checks if the mouse is over any of the buttons.

        :return: A tuple containing the mouse position, grid coordinates, and flags for grid and button presence.
        :rtype: tuple[tuple, int, int, bool, bool]
        """
        mouse_pos = pygame.mouse.get_pos()
        pos_x = math.floor(mouse_pos[0] / (self.square_size + self.spacing))
        pos_y = math.floor(mouse_pos[1] / (self.square_size + self.spacing))
        in_grid = (0 <= pos_x < self.grid.width) and (0 <= pos_y < self.grid.height)
        over_button = any(button.rect.collidepoint(mouse_pos) for button in self.buttons)
        
        return mouse_pos, pos_x, pos_y, in_grid, over_button


    def _set_button_mode(self, pos_x: int, pos_y: int, state_enum: State) -> None:
        """
        Set the state of a square in the grid to a specific state.
        This function changes the state of a square in the grid based on the mouse position
        and the specified state enum. It also updates the application state to reflect
        that the user is no longer in set mode for start or goal.

        :param pos_x: The x-coordinate of the square in grid terms.
        :type pos_x: int
        :param pos_y: The y-coordinate of the square in grid terms.
        :type pos_y: int
        :param state_enum: The state to set for the square (START or GOAL).
        :type state_enum: State
        """
        self.grid.change_state(pos_y, pos_x, state_enum)
        self.local_app_state.set_goal_mode = False
        self.local_app_state.set_start_mode = False
        self.local_app_state.block_action = True


    def _reset_button(self) -> None:
        """
        Reset the grid to its latest relevant state.
        This function resets the grid to the state it was in before the last algorithm was run
        or fully resets it if no algorithm has been run yet. It also updates the application state
        to indicate that no algorithm is currently running and that the grid has been fully reset.
        """

        self.local_app_state.runned_algorithm = False

        # Restore grid
        if self.local_app_state.grid_full_reset == False:
            for row in range(self.grid.height):
                for col in range(self.grid.width):
                    self.grid.get((row, col)).change_state(self.grid_reset_state[row][col])
            self.local_app_state.grid_full_reset = True
        else:
            for row in range(self.grid.height):
                for col in range(self.grid.width):
                    self.grid.get((row, col)).change_state(State.ACTIVATED)


    def handle_button_click(self, idx: int) -> None:
        """
        Handle button click events based on the index of the button clicked.
        This function updates the application state and initializes the algorithms.
        
        :param idx: The index of the button clicked.
        :type idx: int
        """
        
        # Deselect start and goal modes if any button is clicked
        self.local_app_state.set_start_mode = False
        self.local_app_state.set_goal_mode = False
        self.local_app_state.block_action = True

        if idx == 0: # Activate start mode
            # If an algorithm has been runned before, reset the grid
            if self.local_app_state.runned_algorithm:
                self._reset_button()
            self.local_app_state.set_start_mode = True
            self.local_app_state.set_goal_mode = False
        elif idx == 1: # Activate goal mode
            # If an algorithm has been runned before, reset the grid
            if self.local_app_state.runned_algorithm:
                self._reset_button()
            self.local_app_state.set_goal_mode = True
            self.local_app_state.set_start_mode = False

        elif idx == 7: # Reset button
            self._reset_button()
        elif idx == 8:  # Maze (Prim) button
            self._reset_button()  # Reset the grid before generating a maze
            generate_maze_prim(self.grid)
            
        else: # Algorithm buttons
            # Manage the state of the application
            if self.grid.get_start() is None or self.grid.get_goal() is None:
                return

            if self.local_app_state.runned_algorithm:
                self._reset_button()  # Reset the grid if an algorithm has been runned before

            if not self.local_app_state.runned_algorithm: # If an algorithm is not runned yet
                self.grid_reset_state = copy.deepcopy([[square.state for square in row] for row in self.grid.grid])


            # Set the application state
            self.local_app_state.runned_algorithm = True
            self.local_app_state.grid_full_reset = False
            self.local_app_state.start_time = time.time()
            self.local_app_state.running_algorithm = True

            if idx == 2:
                self.algorithm = BFSAlgorithm(self.grid, self.grid.get_neighbors)
            elif idx == 3:
                self.algorithm = DFSAlgorithm(self.grid, self.grid.get_neighbors)
            elif idx == 4:
                self.algorithm = DijkstraAlgorithm(self.grid, self.grid.get_neighbors,  self.grid.get_moving_cost)
            elif idx == 5:
                self.algorithm = AStarAlgorithm(self.grid, self.grid.get_neighbors, self.grid.get_moving_cost , manhattan_heuristic)
            elif idx == 6:
                self.algorithm = GreedyBestFirstAlgorithm(self.grid, self.grid.get_neighbors, manhattan_heuristic)


    def update_algorithm(self) -> None:
        """
        Update the algorithm state and execution time.
        This function actualize the algorithm step and updates the execution time.
        If the algorithm completes, it highlights the final path calculated by the algorithm.
        """
        self.local_app_state.execution_time = time.time() - self.local_app_state.start_time  # Update execution time
        if not self.algorithm.step():
            self.local_app_state.running_algorithm = False
            self.algorithm.highlight_path()  # Highlight the path after algorithm completes



    def handle_mouse_drag(self) -> None:
        """
        Handle mouse dragging events to change the state of squares in the grid.
        This function checks if the mouse is pressed and updates the state of the
        squares based on the mouse position and the current application state.
        """

        # Get the mouse position and check if it's within the grid
        _, pos_x, pos_y, in_grid, over_button = self._get_mouse_position()
        
        # Get the mouse state
        mouse_state = pygame.mouse.get_pressed()
        # Handle mouse dragging action
        if in_grid and not over_button and mouse_state[0] and not self.local_app_state.block_action:
            # Reset the grid if an algorithm has been runned before
            if self.local_app_state.runned_algorithm:
                self._reset_button()  
            self.grid.change_state(pos_y, pos_x, State.DEACTIVATED)
        elif in_grid and not over_button and mouse_state[2] and not self.local_app_state.block_action:
            # Reset the grid if an algorithm has been runned before
            if self.local_app_state.runned_algorithm:
                self._reset_button()  
            self.grid.change_state(pos_y, pos_x, State.ACTIVATED)


class Grid2DScreen(BaseGridScreen):
    """
    Screen for a 2D grid without customizable costs.
    This class inherits from BaseGridScreen and initializes the grid with customizable_cost set to False.
    
    :param screen: The Pygame surface where the grid is drawn.
    :type screen: pygame.Surface
    :param app_state: The global application state that holds the current state of the app.
    :type app_state: GlobalAppState
    
    Customizable costs are not allowed in this screen.
    """
    def __init__(self, screen: pygame.Surface, app_state: GlobalAppState) -> None:
        # Define the size of the grid
        size = 29
        
        # Calculate the available area for the grid
        grid_area_size = SCREEN_HEIGHT - 2*SPACING

        # Calculate the square size so the grid fits within the available area
        square_size = (grid_area_size - (size - 1) * SPACING) // size
        
        # Calculate the total height of the grid and the offset for centering it vertically
        total_grid_height = size * square_size + (size - 1) * SPACING
        draw_grid_offset = (SCREEN_HEIGHT - total_grid_height - SPACING - 2) // 2

        super().__init__(screen, app_state, size, customizable_cost=False, square_size=square_size, draw_centering_offset=draw_grid_offset)


class Grid2DWeightedScreen(BaseGridScreen):
    """
    Screen for a 2D grid with customizable costs.
    This class inherits from BaseGridScreen and initializes the grid with customizable_cost set to True.
    
    :param screen: The Pygame surface where the grid is drawn.
    :type screen: pygame.Surface
    :param app_state: The global application state that holds the current state of the app.
    :type app_state: GlobalAppState

    Customizable costs are used in this screen.
    """
    def __init__(self, screen: pygame.Surface, app_state: GlobalAppState) -> None:
        # Define the size of the grid
        size = 19
        
        # Calculate the available area for the grid
        grid_area_size = SCREEN_HEIGHT - 2*SPACING

        # Calculate the square size so the grid fits within the available area
        square_size = (grid_area_size - (size - 1) * SPACING) // size
        
        # Calculate the total height of the grid and the offset for centering it vertically
        total_grid_height = size * square_size + (size - 1) * SPACING
        draw_grid_offset = (SCREEN_HEIGHT - total_grid_height - SPACING - 2) // 2

        super().__init__(screen, app_state, size, customizable_cost=True, square_size=square_size, draw_centering_offset=draw_grid_offset)