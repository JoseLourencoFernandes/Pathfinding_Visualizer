import pygame
from definitions import Color

#Button class
class Button:
    def __init__(self, x, y, w, h, text, color= Color.GRAY, text_color= Color.BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface, font, active = False):
        if active:
            color = (min(self.color[0]+40,255), min(self.color[1]+40,255), min(self.color[2]+40,255))
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)