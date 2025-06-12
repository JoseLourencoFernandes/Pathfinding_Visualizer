from enum import Enum

# Definitions of constants and classes used in the program
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
    LIGHTBLUE = (202,225,255)
    PALEGREEN = (84,139,84)
    ORANGE = (255, 165, 0)
    
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