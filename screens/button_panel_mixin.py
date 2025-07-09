from classes.button import Button
from definitions.grid_constants import *
from definitions.colors import Color
import pygame

class ButtonPanelMixin:
    """ 
    Mixin class to provide button creation functionality for different grid objects.
    This class can be used to create a set of default buttons for various grid objects,
    such as 2D grids, weighted grids, and graphs.
    It includes methods to create buttons for setting start and goal positions,
    running algorithms, resetting the grid, and generating mazes.
    """
    
    def create_default_buttons(self, object, include_maze_button=False):
        """
        Creates a list of default buttons for the specified grid object.
        
        :param object: The type of grid object for which buttons are created (e.g., "2D Grid", "Weighted Grid", "Graph").
        :type object: str
        :param include_maze_button: Boolean indicating whether to include the maze generation button, defaults to False.
        :type include_maze_button: bool
        
        :return: A list of Button objects for the specified grid object.
        :rtype: list[Button]
        """
        
        buttons = [
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), f"Set Start {object}", Color.LIGHTGREEN),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + (GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), f"Set Goal {object}", Color.TOMATO),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 2*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "BFS Algorithm", Color.TANGERINE),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 3*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "DFS Algorithm", Color.TANGERINE),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 4*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "Dijkstra Algorithm", Color.TANGERINE),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 5*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "A* Algorithm", Color.TANGERINE),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 6*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "Greedy Best First Algorithm", Color.TANGERINE),
            Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 7*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "Reset", Color.TANGERINE),
        ]
        
        if include_maze_button:
            buttons.append(
                Button(pygame.Rect(GRID_BUTTON_X, GRID_BUTTON_Y + 8*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT), "Generate Maze (Using Prim Algorithm)", Color.LIGHTBLUE)
            )
        
        return buttons