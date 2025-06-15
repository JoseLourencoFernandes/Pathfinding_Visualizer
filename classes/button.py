import pygame
from definitions.colors import Color

class Button:
    """
    A class to represent a button in the application.
    This class handles the button's position, size, text, color, and drawing functionality.
    It also provides a method to check if the button is clicked based on mouse position.
    
    Attributes:
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        w (int): The width of the button.
        h (int): The height of the button.
        text (str): The text displayed on the button.
        color (tuple): The color of the button in RGB format.
        text_color (tuple): The color of the text in RGB format.
        icon (str): Optional icon to be displayed on the button.
        
    Methods:
        draw(surface, font, active): Draws the button on the given surface using the specified font.
        is_clicked(pos): Checks if the button is clicked based on the mouse position.
    """
    
    def __init__(self, x, y, w, h, text = None, color= Color.GRAY, text_color= Color.BLACK, icon = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.icon = icon

    def draw(self, screen, font, active = False):
        """
        Draws the button on the given screen using the specified font.
        If the button is active, it changes the color slightly to indicate it is activated.
        
        Arguments:
            screen: The screen on which to draw the button.
            font: The font to use for the button text.
            active: A boolean indicating whether the button is active.
        """
        if active:
            color = (min(self.color[0]+40,255), min(self.color[1]+40,255), min(self.color[2]+40,255))
        else:
            color = self.color
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

    def is_clicked(self, pos):
        """
        Checks if the button is clicked based on the mouse position.
        
        Arguments:
            pos: A tuple representing the mouse position (x, y).
            
        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(pos)