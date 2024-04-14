import pygame
from globals import *
from ui.text import Text

pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #, pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font('ui/font/Quicksand-Medium.ttf', 50)
#sound = pygame.mixer.Sound('audio/fdsfds.wav') Maybe use this method if we need

top_text = Text(font, screen)
mid_text = Text(font, screen)
bot_text = Text(font, screen)

eye = pygame.image.load('ui/graphics/eye.png').convert_alpha()
eye_rect = eye.get_rect()
arrow = pygame.image.load('ui/graphics/arrow.jpg').convert_alpha()

def start_ui():
    top_text.set_text("t1")
    top_text.move_text_to(DISPLAY_WIDTH*(5/10), DISPLAY_HEIGHT*(1/10))
    top_text.slide_text(DISPLAY_WIDTH*(20/10), DISPLAY_HEIGHT*(20/10))

    mid_text.set_text("text2")
    mid_text.move_text_to(DISPLAY_WIDTH*(2/10), DISPLAY_HEIGHT*(8/10))
    mid_text.slide_text(DISPLAY_WIDTH*(8/10), DISPLAY_HEIGHT*(2/10))

    bot_text.set_text("text3")
    bot_text.move_text_to(DISPLAY_WIDTH*(4/10), DISPLAY_HEIGHT*(6/10))
    bot_text.slide_text(DISPLAY_WIDTH*(6/10), DISPLAY_HEIGHT*(4/10))

    global event_cnt
    event_cnt = 0

def ui_loop():
    global event_cnt
    dt = clock.tick(60) / 1000 #units are seconds
    #print(f'DT:{dt:0.10f}')

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            event_cnt += 1
            if event_cnt == 1:
                pass
            if event_cnt == 2:
                top_text.animate_text("new message!")
                mid_text.animate_text("konglonglonglong", animation_type = "right")
                bot_text.animate_text("xxxxxxxxxxxxxxxx", animation_type = "right")
            if event_cnt >= 3:
                pygame.quit()
                return False
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

    screen.fill((255, 255, 255))
    top_text.update(dt)
    mid_text.update(dt)
    bot_text.update(dt)
    eye_rect.center = (200, 200)
    screen.blit(eye, eye_rect)
    screen.blit(arrow, (200,200))

    pygame.display.flip()
    return True
