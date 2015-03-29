import random
import time
import pygame
import os
import sys
import math
from operator import itemgetter, attrgetter, methodcaller
from pygame.locals import *
import pygame._view
from machine import *
from bibleothek import *


def main():
    global windowSurface
    windowSurface = None
    windowSurface, mainClock = createWindowSurface()
    background = loadBackground("feld.png")
    cursor["rect"], cursor["picture"] = loadPicture("cursor.png")
    cursor["rect2"], cursor["picture2"] = loadPicture("cursoronhero2.png")

    getBattler(battleState)
    startBattle(battleState)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    LCLICK = True
                if event.button == 2:
                    RCLICK = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    LCLICK = False

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a') and cursor["currentMenu"]:
                    cursor["leftclick"] = True
                if event.key == K_RIGHT or event.key == ord('d') and cursor["currentMenu"]:
                    cursor["rightclick"] = True
                if event.key == K_UP or event.key == ord('w') and cursor["currentMenu"]:
                    cursor["upclick"] = True
                if event.key == K_DOWN or event.key == ord('s') and cursor["currentMenu"]:
                    cursor["downclick"] = True
                if event.key == K_RETURN or event.key == ord('\r') and cursor["currentMenu"]:
                    #cursor["enterclick"] = True
                    pass
                if event.key == K_BACKSPACE or event.key == ord('\b') and cursor["currentMenu"]:
                    #cursor["backclick"] = True
                    pass

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    pass
                if event.key == K_RIGHT or event.key == ord('d'):
                    pass
                if event.key == K_UP or event.key == ord('w'):
                    pass
                if event.key == K_DOWN or event.key == ord('s'):
                    pass
                if (event.key == K_RETURN or event.key == ord('\r')) and cursor["currentMenu"]:
                    cursor["enterclick"] = True
                    checkCommand(cursor)
                if event.key == K_BACKSPACE or event.key == ord('\b'):
                    menuBackwards(cursor)
                if event.key == K_SPACE or event.key == ord(" "):
                    checkCommand(cursor)

        battleProcess(battleState, cursor)
        checkBattlerCondition(battleState)

        drawPicture(background)
        drawBattler(battleState)
        drawNotification()
        drawInterface(cursor, battleState)

        pygame.display.flip()

        mainClock.tick(FPS)


if __name__ == "__main__":
    main()
