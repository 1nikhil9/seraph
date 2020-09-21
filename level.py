import pygame, os
import random
from init import *
from enemy import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'wall.png')
        if RESIZE:
            img = os.path.join('img', 'wall_r.png')
        self.image = pygame.image.load(img)
        self.image.convert()

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'ladder.png')
        if RESIZE:
            img = os.path.join('img', 'ladder_r.png')
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'gem.png')
        if RESIZE:
            img = os.path.join('img', 'gem_r.png')
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join('img', 'yuu.png')
        if RESIZE:
            img = os.path.join('img', 'yuu_r.png')
        self.image = pygame.image.load(img)
        self.image.convert_alpha()

        if RESIZE:
            pass
        
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

class Level():
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.dest = pygame.sprite.Group()

        for i in range(0, TILEW):
            self.walls.add(Wall(i*TILE, 0))
            self.walls.add(Wall(i*TILE, (TILEH-1)*TILE))
        for i in range(1, TILEH-1):
            self.walls.add(Wall(0, i*TILE))
            self.walls.add(Wall((TILEW-1)*TILE, i*TILE))

    def draw(self):
        for enemy in self.enemies:
            prob = 57*len(self.balls)
            if not random.randint(0, prob):
                self.balls.add(Ball(enemy.rect.x, enemy.rect.y - 2*TILE, enemy.coeff, random.randint(0,1)))

        self.balls.update(self)
        
        self.walls.draw(screen)
        self.ladders.draw(screen)
        self.gems.draw(screen)
        self.balls.draw(screen)
        self.enemies.draw(screen)

        self.dest.draw(screen)

    def build(self, l):
        f = open(str(l)+'.lvl', 'r')

        for line in f:
            l = line.split(' ')

            if(l[0] == 'W'):
                y = int(l[1])
                beg = int(l[2])
                end = int(l[3])

                for x in range(beg, end+1):
                    self.walls.add(Wall(x*TILE, y*TILE))
            
            if(l[0] == 'L'):
                x = int(l[2])
                beg = int(l[1])
                end = beg+4

                for y in range(beg, end+1, 2):
                    self.ladders.add(Ladder(x*TILE, y*TILE))

            if(l[0] == 'G'):
                x = int(l[1])
                y = int(l[2])

                self.gems.add(Gem(x*TILE, y*TILE))

            if(l[0] == 'E'):
                who = l[1]
                x = int(l[2])
                y = int(l[3])
                c = int(l[4])

                self.enemies.add(Enemy(x*TILE, y*TILE, who, c))

            if(l[0] == 'T'):
                x = int(l[1])
                y = int(l[2])

                self.dest.add(Target(x*TILE, y*TILE))
