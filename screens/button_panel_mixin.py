from classes.button import Button
from definitions.grid_constants import *
from definitions.colors import Color

class ButtonPanelMixin:
    def create_default_buttons(self, object, include_maze_button=False):
        buttons = [
            Button(GRID_BUTTON_X, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, f"Set Start {object}", Color.LIGHTGREEN),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + (GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, f"Set Goal {object}", Color.TOMATO),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 2*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "BFS Algorithm", Color.TANGERINE),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 3*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "DFS Algorithm", Color.TANGERINE),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 4*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "Dijkstra Algorithm", Color.TANGERINE),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 5*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "A* Algorithm", Color.TANGERINE),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 6*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "Greedy Best First Algorithm", Color.TANGERINE),
            Button(GRID_BUTTON_X, GRID_BUTTON_Y + 7*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "Reset", Color.TANGERINE),
        ]
        
        if include_maze_button:
            buttons.append(
                Button(GRID_BUTTON_X, GRID_BUTTON_Y + 8*(GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACING), GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, "Generate Maze (Using Prim Algorithm)", Color.LIGHTBLUE)
            )
        
        return buttons