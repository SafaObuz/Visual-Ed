import pygame
from globals import *

class Text:
    def __init__(self, font, color = DEFAULT_TEXT_COLOR, bg = DEFAULT_BG_COLOR):
        self._message = ''
        self._next_message = ''
        self._state = "static"
        self._font = font
        self._antialias = True
        self._color = color
        self._bg = bg #make sure the background color matches for fast AA, hence globals
        self._x : float = 0
        self._y : float = 0
        self._next_x : float = 0
        self._next_Y : float = 0
        self._dx : float = 0
        self._dy : float = 0
        self._time_sum = 0

    def move_text_to(self, x, y):
        self._x = x
        self._y = y
        self._next_x = x
        self._next_y = y
    
    def slide_text(self, x, y):
        self._next_x = x
        self._next_y = y
    
    def set_text_vel(self, x, y):
        self._dx = x
        self._dy = y

    def set_text(self, message):
        self._message = message
        self._next_message = message
        self._state = "static"

    def animate_text(self, message, animation_type = "left"):
        if animation_type == "left":
            self._next_message = message
            self._state = "left_clear"
        if animation_type == "right":
            self._next_message = message
            self._state = "right_clear"
    
    def is_animating(self):
        return self._state == 'static'
    
    def display_text(self):
        text_surface = self._font.render(self._message, self._antialias, self._color, self._bg) #bg is supplied for fast aa
        text_rectangle = text_surface.get_rect(center = (self._x, self._y))
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    def update(self, dt):
        self._x += self._dx * dt
        self._y += self._dy * dt
        self._time_sum += dt
        print("vals", self._y, self._next_y)


        if self._next_x != self._x or self._next_y != self._y:
            self.set_text_vel(self._next_x - self._x, self._next_y - self._y)
            if abs(self._next_x - self._x) < 5:
                self.move_text_to(self._next_x, self._y)
            if abs(self._next_y - self._y) < 5:
                self.move_text_to(self._x, self._next_y)

        if self._time_sum >= ANIMATION_SPEED:
            self._time_sum = 0
            if self._message != self._next_message:
                if self._state == "right_clear":
                    self._message = self._message[:len(self._message) - 1]
                    if self._message == '':
                        self._state = "right_load"
                if self._state == "right_load":
                    self._message = self._next_message[:len(self._message) + 1]
                if self._state == "left_clear":
                    self._message = self._message[1:len(self._message)]
                    if self._message == '':
                        self._state = "left_load"
                if self._state == "left_load":
                    self._message = self._next_message[len(self._next_message) - len(self._message) - 1:len(self._next_message)]

            if self._message == self._next_message:
                self._state = "static"


        self.display_text()




