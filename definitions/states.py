"""
This module defines the states for each square in a grid-based pathfinding algorithm.
"""

from enum import Enum

class SquareState(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    START = 2
    GOAL = 3
    VISITED = 4
    PATH = 5
    FRONTIER = 6
    
    def is_deactivated(self):
        return self == SquareState.DEACTIVATED
    
    def is_activated(self):
        return self == SquareState.ACTIVATED

    def is_start(self):
        return self == SquareState.START

    def is_goal(self):
        return self == SquareState.GOAL

    def is_visited(self):
        return self == SquareState.VISITED

    def is_path(self):
        return self == SquareState.PATH

    def is_frontier(self):
        return self == SquareState.FRONTIER


class SquareState(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    START = 2
    GOAL = 3
    VISITED = 4
    PATH = 5
    FRONTIER = 6
    
    def is_deactivated(self):
        return self == SquareState.DEACTIVATED
    
    def is_activated(self):
        return self == SquareState.ACTIVATED
    
    def is_start(self):
        return self == SquareState.START
    
    def is_goal(self):
        return self == SquareState.GOAL
    
    def is_visited(self):
        return self == SquareState.VISITED
    
    def is_path(self):
        return self == SquareState.PATH
    
    def is_frontier(self):
        return self == SquareState.FRONTIER
