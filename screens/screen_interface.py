import pygame
from app_state import GlobalAppState

class ScreenInterface:
    """
    Abstract base class for all screens in the application.
    This class defines the interface that all screen classes must implement.
    It includes methods for handling events, processing events, running the screen logic,
    and drawing the screen.
    
    :param screen: The Pygame surface where the screen will be drawn.
    :type screen: pygame.Surface
    :param app_state: The global application state that holds the current state of the app.
    :type app_state: GlobalAppState
    """

    def __init__(self, screen: pygame.Surface, app_state: GlobalAppState) -> None:
        """ Constructor for the ScreenInterface class. """
        self.screen = screen
        self.app_state = app_state

    def process_events(self) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError

    def draw(self) -> None:
        raise NotImplementedError
    