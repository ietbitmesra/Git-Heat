
# coding: utf-8

# In[3]:


import pygame
from pygame.locals import * 
from random import randint
import time


class Maze():

    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.size = [1200, 700]
        self.width = 20
        self.height = 20
        self.margin = 1
        self.score = 0
        self.level = 1
        self.grid = []
        self.walls = []
        self.countfinal = 0
        self.make()
        self.gameDisplay = pygame.display.set_mode(self.size)
        self.dark_grey = (50, 50, 50)
        self.gold = (246, 253, 49)
        self.bright_green = (0, 200, 0)
        self.bright_red = (200, 0, 0)
        self.light_blue = (0, 0, 200)
        self.brown = (100,30,30)
        self.grey = (211, 211, 211)
        self.clock = pygame.time.Clock()

    def make(self):
        for i in range(2, 4):
            for j in range(5, 14):
                self.walls.append([i, j])
        for i in range(3, 5):
            for j in range(7, 20):
                self.walls.append([j, i])
        for i in range(10, 12):
            for j in range(10, 15):
                self.walls.append([j, i])
        for i in range(17, 19):
            for j in range(0, 21):
                self.walls.append([j, i])
        for i in range(26, 28):
            for j in range(0, 13):
                self.walls.append([i, j])
        for i in range(4, 6):
            for j in range(31, 35):
                self.walls.append([j, i])
        for i in range(38, 40):
            for j in range(2, 21):
                self.walls.append([i, j])
        for i in range(29, 31):
            for j in range(18, 30):
                self.walls.append([i, j])
        for i in range(5, 7):
            for j in range(24, 30):
                self.walls.append([i, j])
        for i in range(23, 25):
            for j in range(10, 25):
                self.walls.append([j, i])

        for row in range(30):
            self.grid.append([])
            for column in range(40):
                self.grid[row].append(0)
        for wall in self.walls:
            self.grid[wall[1]][wall[0]] = 1
            return self

    def scoredisp(self):
        scoretext = self.scorefont.render("Score: " + (str)(self.score),
                                          1, self.green)
        self.gameDisplay.blit(scoretext, (30, 650))

    def leveldisp(self):
        leveltext = self.scorefont.render("Level: " + (str)(self.level),
                                          1, self.green)
        self.gameDisplay.blit(leveltext, (600, 650))

    def reset(self):
        self.grid = []
        self.walls = []
        self.countfinal = 0
        self.make()
        return self

    def dispmaze(self):
        for row in range(30):
            for column in range(40):
                color = self.dark_grey
                pygame.draw.rect(self.gameDisplay, color, [(self.margin + self.width) * column + self.margin,
                                                      (self.margin + self.height) * row + self.margin,
                                                      self.width,
                                                      self.height])
                color = self.blue
                if self.grid[row][column] == 1:
                    self.countfinal = self.countfinal + 1
                else:
                    pygame.draw.rect(self.gameDisplay, color, [(self.margin + self.width) * column + self.margin + 7,
                                                          (self.margin + self.height) * row + self.margin + 7,
                                                          self.width - 14,
                                                          self.height - 14])

    def drawwalls(self):
        for wall in self.walls:
            pygame.draw.rect(self.gameDisplay, self.grey, [(self.margin + self.width) * wall[0] + self.margin,
                                                      (self.margin + self.height) * wall[1] + self.margin,
                                                      self.width, self.height])

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()


    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))
        smallText = pygame.font.SysFont('Comic Sans MS', 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gameDisplay.blit(textSurf, textRect)



    def game_intro(self):
        self.gameDisplay.fill((255, 255, 255))
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
            myfont = pygame.font.SysFont('Comic Sans MS', 115)
            textsurface = myfont.render('MazeRunner', False, (0, 0, 0))
            self.gameDisplay.blit(textsurface, (330, 280))
            self.button("GO!", 350, 450, 100, 50, self.green, self.bright_green, game_loop)
            self.button("Quit", 675, 450, 100, 50, self.red, self.bright_red, quitgame)

            pygame.display.update()
            self.clock.tick(30)

    def crash(self):
        self.gameDisplay.fill((255, 0, 0))
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.text_objects("Game Over", largeText)
        TextRect.center = ((600), (350))
        self.gameDisplay.blit(TextSurf, TextRect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.button("Play Again", 400, 450, 100, 50, self.green, self.bright_green, game_loop)
            self.button("Quit", 710, 450, 100, 50, self.blue, self.light_blue, quitgame)

            pygame.display.update()
            self.clock.tick(15)



class Person(Maze):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def checkWall(self, x, y, W):
        if [x, y] in W:
            return True
        else:
            return False

    def moveleft(self, W):
        if self.x > 0:
            if self.checkWall(self.x - 1, self.y, W):
                self.x = self.x
            else:
                self.x = (self.x) - 1
        return self

    def moveright(self, W):
        if self.x < 39:
            if self.checkWall(self.x + 1, self.y, W):
                self.x = self.x
            else:
                self.x = (self.x) + 1
        return self

    def moveup(self, W):
        if self.y > 0:
            if self.checkWall(self.x, self.y - 1, W):
                self.y = self.y
            else:
                self.y = (self.y) - 1
        return self

    def movedown(self, W):
        if self.y < 29:
            if self.checkWall(self.x, self.y + 1, W):
                self.y = self.y
            else:
                self.y = (self.y) + 1
        return self


class Ghost(Person):

    def __init__(self):
        x = randint(0, 27)
        y = randint(13, 16)
        Person.__init__(self, x, y)

    def resetghost(self):
        x = randint(0, 27)
        y = randint(13, 16)
        Person.__init__(self, x, y)
        return self

    def ghleft(self, Wa):
        Person.moveleft(self, Wa.walls)
        return self

    def ghright(self, Wa):
        Person.moveright(self, Wa.walls)
        return self

    def ghup(self, Wa):
        Person.moveup(self, Wa.walls)
        return self

    def ghdown(self, Wa):
        Person.movedown(self, Wa.walls)
        return self

    def pos(self, G):
        pygame.draw.rect(G.gameDisplay, G.red, [(G.margin + G.width) * self.x + G.margin,
                                           (G.margin + G.height) * self.y + G.margin,
                                           G.width, G.height])

    def ghostPosition(self, G):
        move = randint(0, 3)
        if move == 0:
            self.ghleft(G)
        elif move == 1:
            self.ghright(G)
        elif move == 2:
            self.ghup(G)
        elif move == 3:
            self.ghdown(G)


class Pacman(Person):

    def __init__(self):
        x = randint(0, 6)
        y = randint(0, 4)
        Person.__init__(self, x, y)

    def resetpacman(self):
        x = randint(0, 6)
        y = randint(0, 4)
        Person.__init__(self, x, y)

    def collectCoin(self, Wa):
        if Wa.grid[self.y][self.x] == 0:
            return True
        else:
            return False

    def pacleft(self, Wa):
        Person.moveleft(self, Wa.walls)
        if self.collectCoin(Wa):
            Wa.grid[self.y][self.x] = 1
            Wa.score += 1
            return self

    def pacright(self, Wa):
        Person.moveright(self, Wa.walls)
        if self.collectCoin(Wa):
            Wa.grid[self.y][self.x] = 1
            Wa.score += 1
            return self

    def pacup(self, Wa):
        Person.moveup(self, Wa.walls)
        if self.collectCoin(Wa):
            Wa.grid[self.y][self.x] = 1
            Wa.score += 1
            return self

    def pacdown(self, Wa):
        Person.movedown(self, Wa.walls)
        if self.collectCoin(Wa):
            Wa.grid[self.y][self.x] = 1
            Wa.score += 1
            return self

    def pos(self, G):
        pygame.draw.rect(G.gameDisplay, G.green, [(G.margin + G.width) * self.x + G.margin,
                                             (G.margin + G.height) * self.y + G.margin,
                                             G.width, G.height])

    def checkGhost(self, V):
        if [self.x, self.y] == [V.x, V.y]:
            return True
        else:
            return False

    def pacPosition(self, G):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pacleft(G)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pacright(G)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pacup(G)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pacdown(G)



class Maze1(Maze):

    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.size = [1200, 700]
        self.width = 20
        self.height = 20
        self.margin = 1
        self.score = 0
        self.level = 2
        self.grid = []
        self.walls = []
        self.countfinal = 0
        self.make()
        self.gameDisplay = pygame.display.set_mode(self.size)
        self.dark_grey = (50, 50, 50)
        self.gold = (246, 253, 49)
        self.bright_green = (0, 200, 0)
        self.bright_red = (200, 0, 0)
        self.light_blue = (0, 0, 200)
        self.brown = (100,30,30)
        self.grey = (211, 211, 211)
        self.clock = pygame.time.Clock()

    def make(self):
        for i in range(2, 4):
            for j in range(0, 12):
                self.walls.append([i, j])
        for i in range(11, 13):
            for j in range(2, 12):
                self.walls.append([i, j])
        for i in range(6, 8):
            for j in range(7, 17):
                self.walls.append([j, i])
        for i in range(15, 17):
            for j in range(0, 23):
                self.walls.append([j, i])
        for i in range(26, 28):
            for j in range(0, 13):
                self.walls.append([i, j])
        for i in range(14, 16):
            for j in range(31, 35):
                self.walls.append([j, i])
        for i in range(38, 40):
            for j in range(6, 27):
                self.walls.append([i, j])
        for i in range(22, 24):
            for j in range(18, 30):
                self.walls.append([j, i])
        for i in range(5, 7):
            for j in range(24, 30):
                self.walls.append([i, j])
        for i in range(12, 14):
            for j in range(20, 27):
                self.walls.append([i, j])

        for row in range(30):
            self.grid.append([])
            for column in range(40):
                self.grid[row].append(0)
        for wall in self.walls:
            self.grid[wall[1]][wall[0]] = 1
            return self

    def dispmaze(self):
        for row in range(30):
            for column in range(40):
                color = self.black
                pygame.draw.rect(self.gameDisplay, color, [(self.margin + self.width) * column + self.margin,
                                                      (self.margin + self.height) * row + self.margin,
                                                      self.width,
                                                      self.height])
                color = self.gold
                if self.grid[row][column] == 1:
                    self.countfinal = self.countfinal + 1
                else:
                    pygame.draw.rect(self.gameDisplay, color, [(self.margin + self.width) * column + self.margin + 7,
                                                          (self.margin + self.height) * row + self.margin + 7,
                                                          self.width - 14,
                                                          self.height - 14])

    def drawwalls(self):
        for wall in self.walls:
            pygame.draw.rect(self.gameDisplay, self.blue, [(self.margin + self.width) * wall[0] + self.margin,
                                                      (self.margin + self.height) * wall[1] + self.margin,
                                                      self.width, self.height])



class Person1(Maze):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def checkWall(self, x, y, W):
        if [x, y] in W:
            return True
        else:
            return False

    def moveleft(self, W):
        if self.x > 0:
            if self.checkWall(self.x - 1, self.y, W):
                self.x = self.x
            else:
                self.x = (self.x) - 1
        return self

    def moveright(self, W):
        if self.x < 39:
            if self.checkWall(self.x + 1, self.y, W):
                self.x = self.x
            else:
                self.x = (self.x) + 1
        return self

    def moveup(self, W):
        if self.y > 0:
            if self.checkWall(self.x, self.y - 1, W):
                self.y = self.y
            else:
                self.y = (self.y) - 1
        return self

    def movedown(self, W):
        if self.y < 29:
            if self.checkWall(self.x, self.y + 1, W):
                self.y = self.y
            else:
                self.y = (self.y) + 1
        return self


class Ghost1(Ghost):

    def __init__(self):
        x = randint(20, 27)
        y = randint(15, 22)
        Person1.__init__(self, x, y)

    def resetghost(self):
        x = randint(20, 27)
        y = randint(15, 22)
        Person1.__init__(self, x, y)
        return self



class Pacman1(Pacman):

    def __init__(self):
        x = randint(0, 1)
        y = randint(0, 1)
        Person1.__init__(self, x, y)

    def resetpacman(self):
        x = randint(0, 1)
        y = randint(0, 1)
        Person1.__init__(self, x, y)


def quitgame():
    pygame.quit()
    quit()

def game_loop():
    GAME = Maze()
    HERO = Pacman()
    VILLIAN = Ghost()
    VILLIAN2 = Ghost()
    GAME.scorefont = pygame.font.Font(None, 30)
    done = False
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    done = True
        HERO.pacPosition(GAME)
        GAME.gameDisplay.fill(GAME.black)
        VILLIAN.ghostPosition(GAME)
        VILLIAN2.ghostPosition(GAME)
        move = randint(0, 3)
        GAME.countfinal = 0
        GAME.dispmaze()
        GAME.drawwalls()
        HERO.pos(GAME)
        VILLIAN.pos(GAME)
        VILLIAN2.pos(GAME)
        if HERO.checkGhost(VILLIAN) or HERO.checkGhost(VILLIAN2):
            GAME.crash()
        elif GAME.countfinal == 967:
            game_loop1()

        GAME.scoredisp()
        GAME.leveldisp()
        GAME.clock.tick(10)
        pygame.display.flip()
    pygame.quit()

def game_loop1():
    GAME = Maze1()
    HERO = Pacman1()
    VILLIAN = Ghost1()
    VILLIAN2 = Ghost1()
    VILLIAN3 = Ghost1()
    GAME.scorefont = pygame.font.Font(None, 30)
    done = False
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    done = True
        HERO.pacPosition(GAME)
        GAME.gameDisplay.fill(GAME.black)
        VILLIAN.ghostPosition(GAME)
        VILLIAN2.ghostPosition(GAME)
        VILLIAN3.ghostPosition(GAME)
        move = randint(0, 3)
        GAME.countfinal = 0
        GAME.dispmaze()
        GAME.drawwalls()
        HERO.pos(GAME)
        VILLIAN.pos(GAME)
        VILLIAN2.pos(GAME)
        VILLIAN3.pos(GAME)
        if HERO.checkGhost(VILLIAN) or HERO.checkGhost(VILLIAN2) or HERO.checkGhost(VILLIAN3):
            GAME.crash()

        GAME.scoredisp()
        GAME.leveldisp()
        GAME.clock.tick(10)
        pygame.display.flip()
    pygame.quit()


pygame.init()
GAME = Maze()
GAME.game_intro()
