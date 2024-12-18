import pygame
from os.path import join
from random import randint , uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HIEGHT / 2))
        self.dir = pygame.math.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cool_down_duration = 400

    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cool_down_duration:
                self.can_shoot = True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.dir = self.dir.normalize() if self.dir else self.dir
        self.rect.center += self.dir * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_time()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups , surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HIEGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos, *groups):
        super().__init__(*groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.init_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.dir = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        self.speed_rotation = randint(40,80)
        self.rotation = 0

    def update(self,dt):
        self.rect.center += self.dir * self.speed * dt
        current_time = pygame.time.get_ticks()
        if current_time - self.init_time >= self.life_time:
            self.kill()

        self.rotation += self.speed_rotation * dt 
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosions(pygame.sprite.Sprite):
    def __init__(self,pos,frames ,*groups):
        super().__init__(*groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
    def update(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def colliosioins():
    global running
    global score

    collision_sprites = pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask)
    if collision_sprites:
        damage_sound.play()
        running = False
    for laser in laser_sprites:
        collied_sprites = pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collied_sprites:
            laser.kill()
            AnimatedExplosions( laser.rect.midtop,explotions_frames ,all_sprites)
            explosion_sound.play()
            score += 10
    

def display_score():
    global score
    text_surf = text.render(str(score),True,(240,240,240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HIEGHT - 50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(20,10).move(0,-8),5,10)


#General Setup
pygame.init()
WINDOW_WIDTH,WINDOW_HIEGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()
score = 0

#Imports
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
text = pygame.font.Font(join('images','Oxanium-Bold.ttf'), 50)
explotions_frames = [pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio','damage.ogg'))
game_sound = pygame.mixer.Sound(join('audio','game_music.wav'))
game_sound.set_volume(0.5)
game_sound.play(loops= -1)

#Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites , star_surf)
player = Player(all_sprites)

#Custom Events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)

while running:
    dt = clock.tick() / 1000
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf,(randint(0,WINDOW_WIDTH),randint(-200,-100)),(all_sprites,meteor_sprites))

    #Update
    all_sprites.update(dt)
    colliosioins()

    #Draw Game
    display_surface.fill('#3a2e3f')

    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()