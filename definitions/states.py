"""
This module defines the states for each square in a grid-based pathfinding algorithm.
"""

from enum import Enum

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
