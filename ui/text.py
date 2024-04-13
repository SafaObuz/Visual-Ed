import pygame
from globals import *

class Text:
    def __init__(self, font, color = DEFAULT_TEXT_COLOR, bg = DEFAULT_BG_COLOR):
        self._message = ''
        self._font = font
        self._antialias = True
        self._color = color
        self._bg = bg #make sure the background color matches for fast AA, hence globals
        self._x : float = 0
        self._y : float = 0
        self._dx : float = 0
        self._dy : float = 0

    def move_text_to(self, x, y):
        self._x = x
        self._y = y
    
    def set_text_vel(self, x, y):
        self._dx = x
        self._dy = y

    def set_text(self, message):
        self._message = message
    
    def display_text(self):
        text_surface = self._font.render(self._message, self._antialias, self._color, self._bg) #bg is supplied for fast aa
        text_rectangle = text_surface.get_rect(center = (self._x, self._y))
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    def update(self, dt):
        # print(self._x)
        # print(self._y)
        self._x += self._dx * dt
        self._y += self._dy * dt

        self.display_text()




