import pygame
from globals import *
from ui.text import Text

pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #, pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font('ui/font/Quicksand-Medium.ttf', 50)
#sound = pygame.mixer.Sound('audio/fdsfds.wav') Maybe use this method if we need

top_text = Text(font)

def start_ui():
    top_text.set_text("testing")
    top_text.move_text_to(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/10)
    top_text.set_text_vel(0, 50)
    global event_cnt
    event_cnt = 0



def ui_loop():
    global event_cnt
    dt = clock.tick(60) / 1000
    #print(f'DT:{dt:0.10f}')

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            event_cnt += 1
            if event_cnt == 1:
                top_text.set_text_vel(0, 0)
            if event_cnt == 2:
                top_text.set_text("new message!")
            if event_cnt >= 3:
                pygame.quit()
                return False
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

    screen.fill(DEFAULT_BG_COLOR)

    top_text.update(dt)

    pygame.display.flip()

    return True
