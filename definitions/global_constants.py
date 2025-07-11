"""
Definitions of constants and classes used in the program.
This module contains constants for global settings of navigation
and screen properties, as well as an enumeration for different screens.
"""

from enum import Enum, auto

# Screen Dimensions Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 701

# Screen Enum to represent different screens in the application
class Screen(Enum):
    MAIN_MENU = auto()
    GRID_2D = auto()
    GRID_2D_WEIGHTED = auto()
    GRAPH = auto()
    GRAPH_WEIGHTED = auto()
