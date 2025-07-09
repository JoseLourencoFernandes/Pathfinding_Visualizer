"""
This module defines the states for each square in a grid-based pathfinding algorithm.
"""

from enum import Enum
from definitions.colors import Color

class State(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    START = 2
    GOAL = 3
    VISITED = 4
    PATH = 5
    FRONTIER = 6
    
    
    def is_deactivated(self):
        return self == State.DEACTIVATED
    
    def is_activated(self):
        return self == State.ACTIVATED
    
    def is_start(self):
        return self == State.START
    
    def is_goal(self):
        return self == State.GOAL
    
    def is_visited(self):
        return self == State.VISITED
    
    def is_path(self):
        return self == State.PATH
    
    def is_frontier(self):
        return self == State.FRONTIER
    
    def get_color(self):
        return State._color_map[self]

    def should_show_cost(self):
        return self in {State.ACTIVATED, State.VISITED, State.PATH, State.FRONTIER}

State._color_map = {
    State.DEACTIVATED: Color.BROWN,
    State.ACTIVATED: Color.GRAY,
    State.START: Color.GREEN,
    State.GOAL: Color.RED,
    State.VISITED: Color.PALEGREEN,
    State.PATH: Color.LIGHTBLUE,
    State.FRONTIER: Color.ORANGE,
}