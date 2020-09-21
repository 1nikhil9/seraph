import pygame, os
from init import *

f = 1
if RESIZE:
    f *= 2.0/3.0

mv_x = 0.25*f
de_x = 1*f
lim_x = 5*f

gr_y = 0.25*f
lim_y = 10*f
jmp_y = 6*f

cl_ld = 0.25*f
lim_ld = 3*f
de_ld = 1*f

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'mika.png')
        if RESIZE:
            img = os.path.join('img', 'mika_r.png')
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = TILE, (TILEH-3)*TILE
        self.jump, self.ladder = 0, 0
        self.speedx, self.speedy = 0.0, 0.0

        self.lives = 3
        self.score = 0
        self.clear = 0
        
    def update(self, level):
        keypress = pygame.key.get_pressed()

        self.updateX(keypress, level)
        self.updateY(keypress, level)

        collideList = pygame.sprite.spritecollide(self, level.gems, True)
        
        self.score += len(collideList)

        collideList1 = pygame.sprite.spritecollide(self, level.balls, False)
        collideList2 = pygame.sprite.spritecollide(self, level.enemies, False)
        
        if collideList1 or collideList2:
            self.lives -= 1

            self.rect.x, self.rect.y = TILE, (TILEH-3)*TILE
            self.jump, self.ladder = 0, 0
            self.speedx, self.speedy = 0.0, 0.0

            level.balls.empty()

        collideList = pygame.sprite.spritecollide(self, level.dest, False)

        if collideList:
            self.rect.x, self.rect.y = TILE, (TILEH-3)*TILE
            self.jump, self.ladder = 0, 0
            self.speedx, self.speedy = 0.0, 0.0
            
            self.clear = 1
            

    def updateX(self, keypress, level):
        if keypress[pygame.K_d]:
            self.speedx += mv_x
        if keypress[pygame.K_a]:
            self.speedx -= mv_x
        if self.speedx > 0 and (not keypress[pygame.K_d]):
            self.speedx = max(self.speedx - de_x, 0)
        if self.speedx < 0 and (not keypress[pygame.K_a]):
            self.speedx = min(self.speedx + de_x, 0)
        
        self.speedx = min(lim_x, self.speedx)
        self.speedx = max(-lim_x, self.speedx)

        self.rect.x += self.speedx

        collideList = pygame.sprite.spritecollide(self, level.walls, False)

        for wall in collideList:
            if self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                self.rect.right = wall.rect.left
                self.speedx = 0
            if self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                self.rect.left = wall.rect.right
                self.speedx = 0
    
    def updateY(self, keypress, level):
        if self.ladder:
            if keypress[pygame.K_w]:
                self.speedy -= cl_ld
            if keypress[pygame.K_s]:
                self.speedy += cl_ld

            if (not keypress[pygame.K_w]) and (not keypress[pygame.K_s]):
                if self.speedy > 0:
                    self.speedy = min(0, self.speedy - de_ld)
                if self.speedy < 0:
                    self.speedy = max(0, self.speedy + de_ld)

            self.speedy = min(self.speedy, lim_ld)
            self.speedy = max(self.speedy, -lim_ld)

            self.rect.y += self.speedy
            
            collideList = pygame.sprite.spritecollide(self, level.walls, False)

            for wall in collideList:
                if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                    self.rect.bottom = wall.rect.top
                    self.speedy = 0
                if self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                    self.speedy = 0
            
            collideList = pygame.sprite.spritecollide(self, level.ladders, False)

            if not collideList:
                self.ladder = 0
        else:
            if not self.jump:
                if keypress[pygame.K_SPACE]:
                    self.speedy -= jmp_y
                    self.jump = 1
            self.speedy += gr_y
            self.speedy = min(self.speedy, lim_y)

            self.rect.y += self.speedy

            collideList = pygame.sprite.spritecollide(self, level.walls, False)

            for wall in collideList:
                if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                    self.rect.bottom = wall.rect.top
                    self.jump = 0
                    self.speedy = 0
                if self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                    self.speedy = 0

            collideList = pygame.sprite.spritecollide(self, level.ladders, False)

            if collideList:
                self.ladder = 1

            for ladder in collideList:
                if len(collideList) == 1 and self.rect.bottom > ladder.rect.top and self.rect.top < ladder.rect.top:
                    if not keypress[pygame.K_s]:
                        self.rect.bottom = ladder.rect.top
                        self.ladder = 0

