import pygame, sys
pygame.init()

RESIZE = 0
TILE = 30
WIDTH = 1920
HEIGHT = 1080

if len(sys.argv) == 2:
    RESIZE = 1
    TILE = (TILE*2)/3
    WIDTH = (WIDTH*2)/3
    HEIGHT = (HEIGHT*2)/3

TILEH = HEIGHT/TILE
TILEW = WIDTH/TILE

WHITE = (255, 255, 255)
GRAY = (190, 190, 190)

screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

background = pygame.Surface(screen.get_size())
background.fill(WHITE)
background.convert()

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)
