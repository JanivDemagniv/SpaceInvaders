import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH,WINDOW_HIEGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
pygame.display.set_caption('Space Shooter')
running = True

#plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x =100

#Importing an images
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_react = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HIEGHT / 2))

star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
star_positions = [(randint(0,1280),randint(0,720)) for i in range(20)]

while running:
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    #Draw Game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    display_surface.blit(player_surf,player_react)
    pygame.display.update()

pygame.quit()