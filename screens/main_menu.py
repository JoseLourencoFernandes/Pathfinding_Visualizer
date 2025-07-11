import pygame
from definitions.global_constants import Screen, SCREEN_WIDTH, SCREEN_HEIGHT
from definitions.colors import Color
from definitions.menu_constants import MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, MENU_BUTTON_SPACING, MENU_BUTTON_X, MENU_BUTTON_Y, TITLE_FONT_SIZE, BUTTON_FONT_SIZE
from classes.button import Button
from screens.screen_interface import ScreenInterface
from app_state import GlobalAppState

class MainMenuScreen(ScreenInterface):
    """
    MainMenuScreen class represents the main menu of the application.
    It inherits from ScreenInterface and handles the display and interaction
    with the main menu, allowing users to choose between different modes.
    
    :param screen: The Pygame surface where the menu is drawn.
    :type screen: pygame.Surface
    :param app_state: The global application state that holds the current state of the app.
    :type app_state: GlobalAppState
    """
    def __init__(self, screen: pygame.Surface, app_state: GlobalAppState) -> None:
        """ Constructor for the MainMenuScreen class. """
        super().__init__(screen, app_state)
        self.title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE, bold=True)
        self.button_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        self.buttons = [
            Button(
                pygame.Rect(
                    MENU_BUTTON_X,
                    MENU_BUTTON_Y,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                "2D Grid",
                Color.LIGHTGREEN
            ),
            Button(
                pygame.Rect(
                    MENU_BUTTON_X,
                    MENU_BUTTON_Y + MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                "2D Grid Weighted",
                Color.LIGHTBLUE
            ),
            Button(
                pygame.Rect(
                    MENU_BUTTON_X,
                    MENU_BUTTON_Y + 2 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING),
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                "Graph",
                Color.LIGHTCORAL
            ),
            Button(
                pygame.Rect(
                    MENU_BUTTON_X,
                    MENU_BUTTON_Y + 3 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING),
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                "Graph Weighted",
                Color.LIGHTCORAL
            )
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles user input events for the main menu.

        :param event: The Pygame event to handle.
        :type event: pygame.event.Event
        """
        # Handle quit event
        if event.type == pygame.QUIT:
            self.app_state.running = False
        # Handle keydown event for quitting with Ctrl+Q
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # Check if any button is clicked
            for idx, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos):
                    if idx == 0:
                        self.app_state.current_screen = Screen.GRID_2D
                    elif idx == 1:
                        self.app_state.current_screen = Screen.GRID_2D_WEIGHTED
                    elif idx == 2:
                        self.app_state.current_screen = Screen.GRAPH
                    elif idx == 3:
                        self.app_state.current_screen = Screen.GRAPH_WEIGHTED

    def run(self) -> None:
        # No specific logic to run for the main menu
        pass

    def draw(self) -> None:
        """
        Draws the main menu on the screen, including the title, subtitle, and buttons.
        """
        self.screen.fill(Color.BLACK)
        # Draw title
        title_surface = self.title_font.render("Pathfinding Visualizer", True, Color.TOMATO)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_surface, title_rect)
        # Draw subtitle
        subtitle_font = pygame.font.SysFont(None, 28)
        subtitle_surface = subtitle_font.render("Choose a mode to start", True, Color.GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, title_rect.bottom + 30))
        self.screen.blit(subtitle_surface, subtitle_rect)
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.button_font)