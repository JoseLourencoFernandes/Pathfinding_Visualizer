import pygame
from definitions.colors import Color

class Button:
    """
    A class to represent a button in the application.
    This class handles the button's position, size, text, color, and drawing functionality.
    It also provides a method to check if the button is clicked based on mouse position.
    
    :param rect: The rectangle defining the button's position and size.
    :type rect: pygame.Rect
    :param text: The text displayed on the button, defaults to None.
    :type text: str, optional
    :param color: The color of the button in RGB format, defaults to Color.GRAY.
    :type color: tuple[int, int, int], optional
    :param text_color: The color of the text in RGB format, defaults to Color.BLACK
    :type text_color: tuple[int, int, int], optional
    :param icon: Optional icon to be displayed on the button.
    :type icon: pygame.Surface, optional
    """
    rect: pygame.Rect
    text: str
    color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    icon: pygame.Surface

    def __init__(self, rect: pygame.Rect, text: str = None, color: tuple[int, int, int] = Color.GRAY, text_color: tuple[int, int, int] = Color.BLACK, icon: pygame.Surface = None) -> None:
        """ Constructor for the Button class. """
        self.rect = rect
        self.text = text
        self.color = color
        self.text_color = text_color
        self.icon = icon

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, active: bool = False) -> None:
        """
        Draws the button on the given screen using the specified font.
        If the button is active, it changes the color slightly to indicate it is activated.
        
        :param screen: The Pygame surface on which to draw the button.
        :type screen: pygame.Surface
        :param font: The font to use for the button text.
        :type font: pygame.font.Font
        :param active: A boolean indicating whether the button is active, defaults to False.
        :type active: bool, optional
        """
        
        # Draw the button rectangle with a color change if active
        color = (min(self.color[0]+40,255), min(self.color[1]+40,255), min(self.color[2]+40,255)) if active else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, Color.BLACK, self.rect, 2)
        
        #Draw text if provided
        if self.text:
            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        #Draw icon if provided
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            screen.blit(self.icon, icon_rect)

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        """
        Checks if the button is clicked based on the mouse position.
        
        :param pos: A tuple representing the mouse position (x, y).
        :type pos: tuple
        
        :returns: True if the button is clicked, False otherwise.
        :rtype: bool
        """
        return self.rect.collidepoint(pos)