from enum import Enum

# Definitions of constants and classes used in the program
# Screen Constants
SPACING = 5
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 701

# Button Constants
BUTTON_WIDTH = 450
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
BUTTON_X = SCREEN_WIDTH - BUTTON_WIDTH - (SCREEN_WIDTH - BUTTON_WIDTH - SCREEN_HEIGHT) / 2 
BUTTON_Y = 20

# Time Text Constants
TIME_TEXT_X = 3/2*(SCREEN_WIDTH - SCREEN_HEIGHT)
TIME_TEXT_Y = 660

# Square Constants
SQUARE_SIZE = 19

# Color Constants
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (102, 205, 0)
    RED = (181, 42, 42)
    GRAY = (50, 50, 50)
    BROWN = (139,115,85)
    LIGHTGREEN = (117, 238, 144)
    TOMATO = (255, 99, 71)
    LIGHTBLUE = (64,198,246)
    PALEGREEN = (84,139,84)
    ORANGE = (255, 165, 0)
    TANGERINE = (255,178,102)
    
# State Enum to represent the state of each square
class State(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    START = 2
    GOAL = 3
    VISITED = 4
    PATH = 5
    FRONTIER = 6
    
    def is_activated(self):
        return self == State.ACTIVATED
    
    def is_start(self):
        return self == State.START
    
    def is_goal(self):
        return self == State.GOAL