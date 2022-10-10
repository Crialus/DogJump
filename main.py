import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.3)

        self.floor = 290
        self.gravity = 0
        self.player_index = 0

        self.player_walk = [player_walk_1,player_walk_2]
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, self.floor))
        
        

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.floor:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.floor: self.rect.bottom = self.floor

    def player_animation(self):
        if self.rect.bottom < self.floor: self.image = self.player_jump
        else: 
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Dog(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'dog':
            dog_1 = pygame.image.load('graphics/dog/dogBrown.png').convert_alpha()
            dog_2 = pygame.image.load('graphics/dog/dogBrownJump.png').convert_alpha()
            dog_3 = pygame.image.load('graphics/dog/dogBrownBend.png').convert_alpha()
        else: pass
        self.frames = [dog_1, dog_2, dog_3]
        self.index = 0
        y_pos = 300
            
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def obstacle_animation(self):
        self.index += 0.1
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.obstacle_animation()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            self.index = 0
            y_pos = 190
        else:
            poo_1 = pygame.image.load('graphics/poo/poo_1.png').convert_alpha()
            poo_2 = pygame.image.load('graphics/poo/poo_2.png').convert_alpha()
            self.frames = [poo_1,poo_2]
            self.index = 0
            y_pos = 300

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def obstacle_animation(self):
        self.index += 0.1
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.obstacle_animation()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SHADOW = (64, 64, 64)
BONE = (225, 225, 225)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
global title
global current_timer
global score
title = 'Riaan Run'
pygame.display.set_caption(f'{title}')
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
game_active = False
score = 0
start_time = 0
current_timer = 0
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
dog_timer = pygame.USEREVENT + 2
pygame.time.set_timer(dog_timer, randint(500, 10000))
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
dog_group = pygame.sprite.Group()
lives_group = pygame.sprite.Group()
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()
heart_image = pygame.image.load('graphics/heartFull.png').convert_alpha()

def display_lives(lives):
    lives_x = [600, 650, 700]
    for life in lives:
        life_rect = heart_image.get_rect(center = (lives_x[life], SCREEN_HEIGHT-30))
        screen.blit(heart_image, life_rect)


def display_timer():
    global current_timer
    current_timer = (pygame.time.get_ticks() - start_time)//1000
    timer_surf = font.render(f'{current_timer}', False, 'red')
    timer_rect = timer_surf.get_rect(center = (SCREEN_WIDTH//2, 30))
    screen.blit(timer_surf, timer_rect)

def collision_sprite():
    global lives
    global score
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,True):
        if len(lives)>1:
            lives.pop()
            return True
        else: return False
    elif pygame.sprite.spritecollide(player.sprite, dog_group, True):
        score += 1
        return True
    
    else: return True

def splash_screen():
    global current_timer
    global score
    player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    title_surf = font.render(f'{title}', False, BONE)
    title_rect = title_surf.get_rect(center = (SCREEN_WIDTH//2, player_stand_rect.top - 20 - title_surf.get_height()//2))
    screen.blit(title_surf, title_rect)
    screen.blit(player_stand, player_stand_rect)
    if current_timer == 0:  
        instruction_surf = font.render('Press any key to start!', False, BONE)
        instruction_rect = instruction_surf.get_rect(center = (SCREEN_WIDTH//2, player_stand_rect.bottom + 20 + instruction_surf.get_height()//2))
        screen.blit(instruction_surf, instruction_rect)
    else: 
        game_over_score_surf = font.render(f'Your score was {score} in {current_timer} seconds', False, BONE)
        game_over_score_rect = game_over_score_surf.get_rect(center = (SCREEN_WIDTH//2, player_stand_rect.bottom + 20 + game_over_score_surf.get_height()//2))
        screen.blit(game_over_score_surf, game_over_score_rect)
        

def display_score(score):
    score_surf = font.render(str(score), False, BONE)
    score_rect = score_surf.get_rect(bottomleft = (20, SCREEN_HEIGHT - 30))
    shadow_surf = font.render(str(score), False, SHADOW)
    shadow_rect = shadow_surf.get_rect(bottomleft = (22, SCREEN_HEIGHT - 28))
    screen.blit(shadow_surf, shadow_rect)
    screen.blit(score_surf,score_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'poo', 'poo', 'poo'])))
            if event.type == dog_timer:
                dog_group.add(Dog('dog'))
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
                score = 0
                lives = [0, 1, 2]
                


    if game_active: 
        screen.blit(sky_surf,(0, 0))
        screen.blit(ground_surf,(0, SCREEN_HEIGHT - ground_surf.get_height()//1.5))
       
        display_timer()
        display_score(score)
        display_lives(lives)

        player.draw(screen)
        obstacle_group.draw(screen)
        dog_group.draw(screen)

        player.update()
        obstacle_group.update()
        dog_group.update()

        

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        splash_screen()

   
      
        

    pygame.display.update()
    clock.tick(60)
 