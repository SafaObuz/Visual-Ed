import pygame
from globals import *
import sys

MIN_TEXT_SPEED = 100

class Text:
    def __init__(self, font, screen, color = DEFAULT_TEXT_COLOR, bg = DEFAULT_BG_COLOR):
        self._message = ''
        self._next_message = ''
        self._state = "static"
        self._font = font
        self._antialias = True
        self._color = color
        self._alpha = 0
        self._alpha_next = 0
        self._bg = bg #make sure the background color matches for fast AA, hence globals
        self._x : float = 0
        self._y : float = 0
        self._next_x : float = 0
        self._next_Y : float = 0
        self._dx : float = 0
        self._dy : float = 0
        self._time_sum = 0
        self._screen = screen
    
    def get_xy(self):
        return (self._x, self._y)

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
    
    def set_alpha(self, alpha):
        self._alpha_next = alpha

    def animate_text(self, message, animation_type = "left"):
        if animation_type == "left":
            self._next_message = message
            self._state = "left_clear"
        if animation_type == "right":
            self._next_message = message
            self._state = "right_clear"
    
    def is_animating(self):
        return self._state != 'static'
    
    def display_text(self):
        text_surface = self._font.render(self._message, self._antialias, self._color, self._bg)
        original_text_rectangle = text_surface.get_rect(center=(self._x, self._y))
        
        # Check if the width exceeds DISPLAY_WIDTH
        if text_surface.get_width() > DISPLAY_WIDTH:
            # Calculate the scaling factor
            scaling_factor = DISPLAY_WIDTH / text_surface.get_width()
            # Scale the text surface
            text_surface = pygame.transform.scale(text_surface, (int(text_surface.get_width() * scaling_factor), int(text_surface.get_height() * scaling_factor)))
            # Recalculate the position of the text rectangle after scaling
            text_rectangle = text_surface.get_rect(center=original_text_rectangle.center)
        else:
            text_rectangle = original_text_rectangle

        text_surface.set_alpha(self._alpha)
        text_surface.set_colorkey(DEFAULT_BG_COLOR)
        self._screen.blit(text_surface, text_rectangle)

    def update(self, dt):
        self._x += self._dx * dt
        self._y += self._dy * dt
        self._time_sum += dt
        
        def sgn(x):
            return (x > 0) - (x < 0)

        if self._next_x != self._x or self._next_y != self._y:
            if abs(self._next_x - self._x) < MIN_TEXT_SPEED:
                x = MIN_TEXT_SPEED*sgn(self._next_x - self._x)
            elif abs(self._next_x - self._x) > MAX_TEXT_SPEED:
                x = MAX_TEXT_SPEED*sgn(self._next_x - self._x)
            else:
                x = self._next_x - self._x
            if abs(self._next_y - self._y) < MIN_TEXT_SPEED:
                y = MIN_TEXT_SPEED*sgn(self._next_y - self._y)
            elif abs(self._next_y - self._y) > MAX_TEXT_SPEED:
                y = MAX_TEXT_SPEED*sgn(self._next_y - self._y)
            else:
                y = self._next_y - self._y

            self.set_text_vel(x, y)

            if abs(self._next_x - self._x) < 0.9:
                self._x = self._next_x
                self._dx = 0
            if abs(self._next_y - self._y) < 0.9:
                self._y = self._next_y
                self._dy = 0

        if self._time_sum >= ANIMATION_SPEED:
            self._time_sum = 0
            if self._message != self._next_message:
                if self._state == "right_clear":
                    if self._message == '':
                        self._state = "right_load"
                    else:
                        self._message = self._message[:len(self._message) - 1]
                if self._state == "right_load":
                    self._message = self._next_message[:len(self._message) + 1]
                if self._state == "left_clear":
                    if self._message == '':
                        self._state = "left_load"
                    else:
                        self._message = self._message[1:len(self._message)]
                if self._state == "left_load":
                    self._message = self._next_message[len(self._next_message) - len(self._message) - 1:len(self._next_message)]

            if self._message == self._next_message:
                self._state = "static"
        
        if self._alpha != self._alpha_next:
            self._alpha += FADE_RATE * dt * sgn(self._alpha_next - self._alpha)
            if abs(self._alpha_next - self._alpha) < 0.9:
                self._alpha = self._alpha

        self.display_text()