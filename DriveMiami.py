# I followed Coding With Russ's pygame scrolling shooter guide series for a blueprint of the project

import os
import random
import pygame
from pygame.locals import *
 
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('DriveMiami')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define player input variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
shoot = False

#define game variables
TILE_SIZE = 48
score = 0
scoreCounter = 0

#load images
#track
track = pygame.image.load('DriveMiami/art/track_bg.png')
#bullets

#item boxes


#define colors
BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)
    
def draw_text(x, y):
    font = pygame.font.SysFont(None, 25, True, True)
    text1 = font.render(f"Score: {score}", False, 'white')
    screen.blit(text1, (x, y))
    font = pygame.font.SysFont(None, 25, True, True)
    text2 = font.render(f"Health: {player.health}", False, 'white')
    screen.blit(text2, (x, y + 20))    




class Track(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, scroll_speed):
        pygame.sprite.Sprite.__init__(self)
        self.framecounter = 0
        self.speed = scroll_speed
        img = track
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale )))
        self.rect = self.image.get_rect()
        self.int_x = x
        self.int_y = y
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += +(self.speed)
        if self.framecounter == 64:
            self.rect.center = (self.int_x, self.int_y)
            self.framecounter = 0



#car class
class Car(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, bullet_type):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.bullet_type = bullet_type
        self.action = 0 
        self.shoot_cooldown = 0
        img = pygame.image.load(f'DriveMiami/art/{self.char_type}')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale )))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        #if self.health > 0:
        print("I'm alive")
            

    def move(self, moving_left, moving_right, moving_up, moving_down):
        #reset movement variables
        dx = 0
        dy = 0

        #assign movement variables if moving left, right, up, or down
        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed
        if moving_up:
            dy = -self.speed
        if moving_down:
            dy = self.speed

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):    
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 10
            bullet = Bullet(self.bullet_type, self.rect.centerx, self.rect.centery - (1.2 * self.rect.size[0]), 3)
            bullet_group.add(bullet)



    def AI(self):
        #checks to see if the car uses enemy bullet type and that the car is alive
        if self.bullet_type == 1 and self.health > 0:
            #enemy attempts to match the player's x value
            if self.rect.centerx < player.rect.centerx:
                self.move(moving_left=False, moving_right=True, moving_up=False, moving_down=False)
            if self.rect.centerx > player.rect.centerx:
                self.move(moving_left=True, moving_right=False, moving_up=False, moving_down=False)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            #self.speed = 0
            #if a car dies then it will start moving off-screen and despawn
            self.alive = False
            self.move(moving_left=False, moving_right=False, moving_up=False, moving_down=True)
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom > SCREEN_HEIGHT:
                self.kill()

        if self.health > 100:
            self.health = 100
            #self.update_action()


    def draw(self):
        screen.blit(self.image, self.rect)


#itembox class
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        img = pygame.image.load(f'DriveMiami/art/item_box_{self.item_type}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale )))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        if pygame.sprite.spritecollide(player, item_group, False):
            if item_type == 0:
                player.health += 25
                self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)
            

#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = 10
        #two directions for bullets
        self.direction = -1
        #two bullet images 0 for player, 1 for enemy
        img = pygame.image.load(f'DriveMiami/art/bullet_{self.char_type}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale )))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #self.direction = direction

    def update(self):
        #move bullet
        self.rect.y += self.speed * self.direction
        #check if bullet have gone off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemies:
                
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 15
                    self.kill()
                



track_bg = Track(300, 400, 3, 6)
bullet_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
player = Car('car_0.png', 50, 50, 3, 5, 0)
enemies = [Car('car_1.png', 200, 200, 3, 3, 1)]
item_health = ItemBox(0, 250, 250, 3)





run = True
while run:

    clock.tick(FPS)

    draw_bg()
    track_bg.update()
    track_bg.draw()
    #counts frames for seamless animation
    track_bg.framecounter += 1

    scoreCounter += 1
    if scoreCounter == FPS:
        score += 1
        scoreCounter = 0

        if score%3 == 0:
            enemies.append(Car('car_1.png', random.randint(100,500), random.randint(100,200), 3, 3, 1))

    player.update()
    player.draw()
    for enemy in enemies:
        enemy.AI()
        enemy.update()
        enemy.draw()
    item_health.update()
    item_health.draw()
    player.move(moving_left, moving_right, moving_up, moving_down)


    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    item_group.update()
    item_group.draw(screen)

    draw_text(20,50)

    if player.alive:
        if shoot:
            player.shoot()
 
 
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
    
        #keyboard pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                shoot = True

                
        #keyboard released    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False          
            if event.key == pygame.K_SPACE:
                shoot = False


    pygame.display.update()

pygame.quit()