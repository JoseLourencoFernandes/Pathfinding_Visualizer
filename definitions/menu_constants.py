"""
Constants for the menu screen of the game.
This module defines constants used in the main menu layout of the application.
"""

from definitions.global_constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Button Constants for the Main Menu
MENU_BUTTON_WIDTH = 320
MENU_BUTTON_HEIGHT = 60
MENU_BUTTON_SPACING = 30
MENU_BUTTON_X = (SCREEN_WIDTH - MENU_BUTTON_WIDTH) // 2
MENU_BUTTON_Y = SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT - MENU_BUTTON_SPACING // 2 + 100

# Font Sizes Constants for the Main Menu
TITLE_FONT_SIZE = 64
BUTTON_FONT_SIZE = 36