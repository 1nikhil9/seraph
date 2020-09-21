from init import *
from player import *
from level import *

class Game:
    def __init__(self):
        self.mika = Player()
        self.char = pygame.sprite.Group()

        self.score = 0
        self.l = 0

    def mainMenu(self):
        loc = os.path.join('img', 'seraph.png')
        if RESIZE:
            loc = os.path.join('img', 'seraph_r.png')

        bg = pygame.image.load(loc).convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        screen.blit(bg, (0,0))
        pygame.display.update()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.startGame()

                    screen.blit(bg, (0,0))
                    pygame.display.update()

                    pygame.time.wait(2000)


    def startGame(self):
        self.score = 0
        self.char.empty()
        self.mika = Player()
        self.char.add(self.mika)

        self.l = 1

        while 1:
            level = Level()
            level.build(self.l)

            if not self.gameRun(level):
                loc = os.path.join('img', 'fail.png')
                if RESIZE:
                    loc = os.path.join('img', 'fail_r.png')
                bg = pygame.image.load(loc).convert()

                screen.blit(bg, (0,0))
                pygame.display.update()
                
                pygame.time.wait(3000)

                break

            self.l += 1
            if self.l == 4:
                loc = os.path.join('img', 'saved.png')
                if RESIZE:
                    loc = os.path.join('img', 'saved_r.png')
                bg = pygame.image.load(loc).convert()

                screen.blit(bg, (0,0))
                pygame.display.update()
                
                pygame.time.wait(3000)

                break

    def gameRun(self, level):
        while 1:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

            screen.blit(background, (0, 0))

            self.mika.update(level)
            self.score += self.mika.score
            self.mika.score = 0

            level.draw()
            self.char.draw(screen)
            

            scoreDisplay = pygame.font.SysFont("None", TILE).render("Score: "+str(self.score), True, (0,0,0)).convert_alpha()
            if self.mika.lives > 1:
                livesDisplay = pygame.font.SysFont("None", TILE).render(str(self.mika.lives)+" lives left", True, (0,0,0)).convert_alpha()
            else:
                livesDisplay = pygame.font.SysFont("None", TILE).render(str(self.mika.lives)+" life left", True, (0,0,0)).convert_alpha()
            levelDisplay = pygame.font.SysFont("None", TILE).render("Level "+str(self.l)+" of 3", True, (0,0,0)).convert_alpha()
            
            screen.blit(scoreDisplay, (TILE*1.5, TILE*1.5))
            screen.blit(livesDisplay, (TILE*1.5, TILE*2.5))
            screen.blit(levelDisplay, (TILE*57, TILE*1.5))

            pygame.display.update()
            
            if not self.mika.lives:
                return 0
            if self.mika.clear:
                self.mika.clear = 0
                return 1

game = Game()
game.mainMenu()
