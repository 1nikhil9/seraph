import pygame, os
import random
from init import *

f = 1
if RESIZE:
    f *= 2.0/3.0

gr_y = 0.25*f
lim_y = 10*f
mv_x = 4*f
jmp_y = 7.5*f

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, coeff, roll):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'ball.png')
        if RESIZE:
            img = os.path.join('img', 'ball_r.png')
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        if RESIZE:
            self.image = pygame.transform.scale(self.image, (TILE, TILE))
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.speedx = coeff * mv_x
        self.speedy = 0

        self.roll = roll

    def update(self, level):
        self.updateX(level)
        self.updateY(level)

    def updateX(self, level):
        self.rect.x += self.speedx

        collideList = pygame.sprite.spritecollide(self, level.walls, False)

        for wall in collideList:
            if self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                self.rect.right = wall.rect.left
                self.speedx = -self.speedx
            if self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                self.rect.left = wall.rect.right
                self.speedx = -self.speedx

                if self.rect.y >= 30*TILE:
                    self.kill()
    
    def updateY(self, level):
        self.speedy += gr_y
        self.speedy = min(self.speedy, lim_y)

        self.rect.y += self.speedy

        collideList = pygame.sprite.spritecollide(self, level.walls, False)

        for wall in collideList:
            if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                self.rect.bottom = wall.rect.top
                self.jump = 0
                if not self.roll:
                    self.speedy = -jmp_y

            if self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                self.rect.top = wall.rect.bottom
                self.speedy = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, who, coeff):
        pygame.sprite.Sprite.__init__(self)
        
        if RESIZE:
            who = who+'_r.png'
        else:
            who = who+'.png'

        img = os.path.join('img', who)
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        if RESIZE:
            pass

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.coeff = coeff
