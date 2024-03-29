# VVhackamole
# By Calvin Probst calvin.probst@gmail.com
# https://github.com/calvinProbstSchool/whackamoleProbst
#

import pygame
import random
import sys
from pygame.locals import *
from pygame.sprite import  *

class DolphinHead(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("dolphinMoleHead.png")
        self.rect = self.image.get_rect()

class VVaveRow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("vvaves.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class PlayButton(pygame.sprite.Sprite):
    def __init__(self, x, y, textFont, message, textColor, bgColor):
        pygame.sprite.Sprite.__init__(self)

        self.image = textFont.render(message,True, textColor, bgColor)

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y


VVINDOVVSIZE = 600
FPS = 300
FONTSIZE = 60

VVHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPBOI = (57,41,140)
BLUEMANGROUP = (33, 195, 200)



def main():
    global FPSCLOCK, DISPLAYSURF, GAMEFONT, ROVV1, ROVV2, ROVV3, ROVV4, STARTGROUP, SUBTIME
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((VVINDOVVSIZE, VVINDOVVSIZE))
    pygame.display.set_caption("VVhack-a-dolphin")
    FPSCLOCK = pygame.time.Clock()
    GAMEFONT = pygame.font.Font('./3Dventure.ttf', FONTSIZE)
    DOLPHINSPRITE = DolphinHead()
    VVAVE1 = VVaveRow(100, 125)
    VVAVE2 = VVaveRow(100, 225)
    VVAVE3 = VVaveRow(100, 325)
    VVAVE4 = VVaveRow(100, 425)
    STARTBUTTON = PlayButton(300, 550, GAMEFONT, "Play VVhackamole", BLUEMANGROUP, VVHITE)
    LEGOYODA = pygame.mixer.Sound("yodaDeathOG.wav")

    mousex = 0
    mousey = 0
    timeGame = 0
    score = 0
    dolPos = 0
    waitTime = 0

    ROVV1 = Group(VVAVE1)
    ROVV2 = Group(VVAVE2)
    ROVV3 = Group(VVAVE3)
    ROVV4 = Group(VVAVE4)
    STARTGROUP = Group(STARTBUTTON)
    gamePlaying = False
    dolphinUp = False
    dolphinDown = False
    dolphinOut = False
    dolphinQuickDown = False
    newDolphinNeeded = False

    SUBTIME = 0

    drawBoard(0, True)

    while True:

        if timeGame > 180:
            gamePlaying = False
            pygame.time.wait(1000)
            main()

        if gamePlaying:
            drawBoard(score, False)
            timeGame =  int((pygame.time.get_ticks() - SUBTIME) / 1000)
        else:
            SUBTIME = pygame.time.get_ticks()


        if newDolphinNeeded:
                dolPos = random.randint(0, 3)
                DOLPHINSPRITE.rect.y = (100 * dolPos) + 88
                DOLPHINSPRITE.rect.x = random.randint(100, 400)
                newDolphinNeeded = False
                dolphinOut = True
                dolphinUp = True
                print(dolPos)
                if dolPos == 0:
                    ROVV1.add(DOLPHINSPRITE)
                elif dolPos == 1:
                    ROVV2.add(DOLPHINSPRITE)
                elif dolPos == 2:
                    ROVV3.add(DOLPHINSPRITE)
                elif dolPos == 3:
                    ROVV4.add(DOLPHINSPRITE)



        if dolphinUp:
            if DOLPHINSPRITE.rect.y > ((dolPos * 100)):
                DOLPHINSPRITE.rect.y -= 1 + (score + 1) / 11
            else:
                dolphinUp = False
                dolphinDown = True

        if dolphinDown:
            if DOLPHINSPRITE.rect.y < ((dolPos * 100) + 88):
                DOLPHINSPRITE.rect.y += 1 + (score + 1) / 11
            else:
                dolphinDown = False
                dolphinOut = False
                newDolphinNeeded = True

        if dolphinQuickDown:
            dolphinOut = False
            if DOLPHINSPRITE.rect.y < ((dolPos * 100) + 88):
                DOLPHINSPRITE.rect.y += 2  * (1 + (score + 1) / 11 )
            else:
                dolphinQuickDown = False
                newDolphinNeeded = True


        buttonPressed = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                buttonPressed = True
                mousex, mousey = event.pos

        if not gamePlaying and buttonPressed:
            if STARTBUTTON.rect.collidepoint(mousex, mousey):
                STARTGROUP.remove(STARTBUTTON)
                gamePlaying = True
                newDolphinNeeded = True
        elif gamePlaying and buttonPressed and abs(mousex - 300) < 201 and abs(mousey - 300) < 201:
            if DOLPHINSPRITE.rect.collidepoint(mousex, mousey) and dolphinOut:
                dolphinOut = False
                dolphinQuickDown = True
                dolphinUp = False
                dolphinDown = False
                score += 1
                LEGOYODA.play(1)
                pygame.time.wait(int(LEGOYODA.get_length() * 1000))



def drawBoard(score, new):
    DISPLAYSURF.fill(BLACK)
    drawClock(new)
    SCORE = GAMEFONT.render(str(score), True, PURPBOI)
    DISPLAYSURF.blit(SCORE, (400, 10))
    pygame.draw.rect(DISPLAYSURF, VVHITE, (100, 100, 400, 400))

    ROVV1.draw(DISPLAYSURF)
    pygame.draw.rect(DISPLAYSURF, VVHITE, (100, 200, 400, 300))

    ROVV2.draw(DISPLAYSURF)
    pygame.draw.rect(DISPLAYSURF, VVHITE, (100, 300, 400, 200))

    ROVV3.draw(DISPLAYSURF)
    pygame.draw.rect(DISPLAYSURF, VVHITE, (100, 400, 400, 100))

    ROVV4.draw(DISPLAYSURF)
    pygame.draw.rect(DISPLAYSURF, BLACK, (100, 500, 400, 100))
    STARTGROUP.draw(DISPLAYSURF)
    pygame.display.update()


def drawClock(new):
    FPSCLOCK.tick(FPS)
    timeNum = int((pygame.time.get_ticks() - SUBTIME) / 1000)
    timeStr = str(int(timeNum % 60))
    timeNum = timeNum - (timeNum % 60)
    minnum = 0
    while timeNum >= 60:
        minnum += 1
        timeNum -= 60
    if len(timeStr) == 1:
        timeStr = "0" + timeStr
    timeStr = str(minnum) + ":" + timeStr
    if new:
        timeStr = "0:00"
    timer = GAMEFONT.render(timeStr, True, BLUEMANGROUP)
    DISPLAYSURF.blit(timer, (10, 10))


main()