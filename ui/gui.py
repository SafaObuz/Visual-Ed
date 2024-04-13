import pygame

pygame.init()

screen = pygame.display.set_mode((480, 800))

clock = pygame.time.Clock()

def ui_loop():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill("red")

    #graphics

    pygame.display.flip()
    clock.tick(60)
