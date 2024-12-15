import pygame

pygame.init()
WINDOW_WIDTH,WINDO_HIEGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDO_HIEGHT))
running = True

while running:
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Draw Game
    display_surface.fill('red')
    pygame.display.update()

pygame.quit()