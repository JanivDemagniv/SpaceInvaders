import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HIEGHT / 2))
        self.dir = pygame.math.Vector2()
        self.speed = 300

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.dir = self.dir.normalize() if self.dir else self.dir
        self.rect.center += self.dir * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('Fire!')

class Star(pygame.sprite.Sprite):
    def __init__(self, groups , surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HIEGHT)))

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

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites , star_surf)
player = Player(all_sprites)


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

    all_sprites.update(dt)

    #Draw Game
    display_surface.fill('darkgray')
    display_surface.blit(meteor_surf,meteor_react)
    display_surface.blit(laser_surf,laser_rect)

    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()