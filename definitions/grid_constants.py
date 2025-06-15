"""
This module defines constants used in the grid and button layout of the application.
It includes dimensions for the grid, buttons, and text, as well as spacing values.
"""

from definitions.global_constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Button Constants for the Grid
GRID_BUTTON_WIDTH = 450
GRID_BUTTON_HEIGHT = 50
GRID_BUTTON_SPACING = 20
GRID_BUTTON_X = SCREEN_WIDTH - GRID_BUTTON_WIDTH - (SCREEN_WIDTH - GRID_BUTTON_WIDTH - SCREEN_HEIGHT) / 2 - 20 
GRID_BUTTON_Y = 20

# Square and Spacing Constants
SQUARE_SIZE = 19
SPACING = 5

# Time Text Constants for the Grid
TIME_TEXT_X = 3/2*(SCREEN_WIDTH - SCREEN_HEIGHT) - 20
TIME_TEXT_Y = 660