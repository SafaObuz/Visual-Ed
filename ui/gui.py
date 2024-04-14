import pygame
from globals import *
from ui.text import Text

pygame.init()
global screen
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #, pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font('ui/font/Quicksand-Medium.ttf', 50)
font_small = pygame.font.Font('ui/font/Quicksand-Medium.ttf', 25)
gpt_message = ''
#sound = pygame.mixer.Sound('audio/fdsfds.wav') Maybe use this method if we need

gpt_top = Text(font, screen)
gpt_mid = Text(font, screen)
gpt_bot = Text(font, screen)
gpt = [gpt_top, gpt_mid, gpt_bot]

a = Text(font_small, screen)
b = Text(font_small, screen)
c = Text(font_small, screen)
d = Text(font_small, screen)
e = Text(font_small, screen)
start_height = 300
multiple_choice = [a, b, c, d, e] #Probably should use pygame Group, but I'd rather not finagle with it... I forget how to use

eye = pygame.image.load('ui/graphics/eye.png').convert_alpha()
eye_original_rect = eye.get_rect()
eye_scale_factor = 0.5
arrow = pygame.image.load('ui/graphics/arrow.png').convert_alpha()
arrow_original_rect = arrow.get_rect()
arrow_scale_factor = 0.25

def scale_arrow():
    scaled_width = int(arrow_original_rect.width * arrow_scale_factor)
    scaled_height = int(arrow_original_rect.height * arrow_scale_factor)
    return pygame.transform.scale(arrow, (scaled_width, scaled_height))

def scale_eye():
    scaled_width = int(eye_original_rect.width * eye_scale_factor)
    scaled_height = int(eye_original_rect.height * eye_scale_factor)
    return pygame.transform.scale(eye, (scaled_width, scaled_height))

arrow_surface = scale_arrow()
arrow_rect = arrow_surface.get_rect()

eye_surface = scale_eye()
eye_rect = eye_surface.get_rect()
global eye_loc
eye_loc = 0

def set_gpt_message(msg: str):
    total_chars = len(msg)
    third_length = total_chars // 3
    # Find the nearest spaces to the third lengths to avoid cutting words
    first_third_end = msg.find(' ', third_length)
    second_third_end = msg.find(' ', 2 * third_length)
    first_third = msg[:first_third_end]
    second_third = msg[first_third_end:second_third_end]
    third_third = msg[second_third_end:]
    for i, g in enumerate(gpt):
        if i == 0:
            g.animate_text(first_third)
        elif i == 1:
            g.animate_text(second_third)
        else:
            g.animate_text(third_third)



def set_multiple_choice_alpha(value : int):
    for i in multiple_choice:
        i.set_alpha(value)

def set_gpt_off_screen():
    for i, g in enumerate(gpt):
        g.move_text_to(DISPLAY_WIDTH/2, -200)


def set_multiple_choice_off_screen():
    for i in range(len(multiple_choice)):
        multiple_choice[i].move_text_to(-DISPLAY_WIDTH * 0.3, start_height + DISPLAY_HEIGHT*(i/12))

def print_multiple_choice(lst : list):
    set_multiple_choice_alpha(255)
    for i, msg in enumerate(lst):
        multiple_choice[i].animate_text(msg)
        multiple_choice[i].slide_text(DISPLAY_WIDTH*(4/10), start_height + DISPLAY_HEIGHT*(i/12))

def render_multiple_choice(dt):
    for i in multiple_choice:
        i.update(dt)

def render_gpt(dt):
    for g in gpt:
        g.update(dt)

def select_multiple_choice(i : int):
    global eye_loc
    eye_loc = i

def move_gpt_onscreen():
    for i, g in enumerate(gpt):
        g.slide_text(DISPLAY_WIDTH/2, 50 + i * 50)
        g.set_alpha(255)

def start_ui():
    set_multiple_choice_alpha(0)
    set_multiple_choice_off_screen()
    set_gpt_off_screen()
    arrow_surface.set_alpha(0)
    eye_surface.set_alpha(0)

    global event_cnt
    event_cnt = 0

def ui_loop():
    global event_cnt
    global eye_loc
    
    dt = clock.tick(60) / 1000 #units in seconds

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            event_cnt += 1
            if event_cnt == 1:
                move_gpt_onscreen()
                print_multiple_choice(["Option 1", "Option B", "Option C", "Option D", "Option E"])
            if event_cnt == 2:
                set_gpt_message("THIS IS A SUPER SUPER DUPER LONG MESSAGE")
                eye_loc = 3
            if event_cnt >= 3:
                pygame.quit()
                return False
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
    if event_cnt == 1:
        arrow_surface.set_alpha(arrow_surface.get_alpha() + FADE_RATE * dt) if arrow_surface.get_alpha() <= 255 else 0
        eye_surface.set_alpha(eye_surface.get_alpha() + FADE_RATE * dt) if eye_surface.get_alpha() <= 255 else 0


    screen.fill((255, 255, 255))

    eye_rect.center = (DISPLAY_WIDTH/8, start_height + DISPLAY_HEIGHT*(eye_loc/12))
    screen.blit(eye_surface, eye_rect)

    arrow_rect.center = (DISPLAY_WIDTH/2, 700)
    screen.blit(arrow_surface, arrow_rect)

    render_multiple_choice(dt)
    render_gpt(dt)

    pygame.display.flip()
    return True
