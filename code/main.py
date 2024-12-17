import pygame
from os.path import join
from random import randint

#General Setup
pygame.init()
WINDOW_WIDTH,WINDOW_HIEGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

#plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x =100

#Importing an images
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_react = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HIEGHT / 2))
player_dir = pygame.math.Vector2()
player_speed = 300

meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_react = meteor_surf.get_frect(center = (WINDOW_WIDTH /2,WINDOW_HIEGHT/2 + 100))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20,WINDOW_HIEGHT - 20))

star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
star_positions = [(randint(0,1280),randint(0,720)) for i in range(20)]

while running:
    dt = clock.tick() / 1000
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Input
    keys = pygame.key.get_pressed()
    player_dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_dir = player_dir.normalize() if player_dir else player_dir
    player_react.center += player_dir * player_speed * dt

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print('Fire!')


    #Draw Game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    display_surface.blit(meteor_surf,meteor_react)
    display_surface.blit(laser_surf,laser_rect)
    display_surface.blit(player_surf,player_react)

    
    pygame.display.update()

pygame.quit()