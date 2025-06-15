class ScreenInterface:
    """
    Abstract base class for all screens in the application.
    This class defines the interface that all screen classes must implement.
    It includes methods for handling events, processing events, running the screen logic,
    and drawing the screen.
    
    Attributes:
        screen (pygame.Surface): The Pygame surface where the screen will be drawn.
        app_state (GlobalAppState): The global application state that holds the current state of the app.
    """
    def __init__(self, screen, app_state):
        self.screen = screen
        self.app_state = app_state

    def process_events(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
    
    def draw(self, screen):
        raise NotImplementedError
    