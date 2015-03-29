import random, time, pygame, os, sys, math
from operator import itemgetter, attrgetter, methodcaller
from pygame.locals import *
import pygame._view

WHITE = (255, 255, 255)
AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CORNFLOWERBLUE = (100, 149, 237)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = ( 192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
HPCOLOUR = (231, 97, 0)
STACOLOUR = (236, 239, 0)
farbe = (BLACK, AQUA, WHITE, BLUE, CORNFLOWERBLUE, FUCHSIA, GRAY,
         GREEN, LIME, MAROON, NAVYBLUE, OLIVE, PURPLE, RED, SILVER, TEAL, YELLOW)

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
FPS = 60
GAMETITLE = "crushonjesus"
VERSION = "0.03b"
MOVESPEED = 5
FRAME = 0
LCLICK = False
RCLICK = False

firstPartyPos = [[320, 440], [496, 550]]
secondPartyPos = [[750, 130], [950, 150], [1100, 270]]
bossPos = [900, 200]
figures = []
numbers = []
notes = []

from bibleothek import *

global windowSurface


def createWindowSurface():
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load("bilder\\icon.ico"))
    global windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption(GAMETITLE + " " + VERSION)
    pygame.mouse.set_visible(0)
    return (windowSurface, mainClock)


def terminate():
    pygame.quit()
    sys.exit()


def loadFont(size, font):
    return pygame.font.SysFont(font, size)


def loadAndDrawText(text, size, xy, color, aa=True, fonty="arial"):
    font = pygame.font.SysFont(fonty, size)
    textobj = font.render(text, aa, color)
    textrect = textobj.get_rect()
    textrect.topleft = xy
    windowSurface.blit(textobj, textrect)
    return textrect


def loadText(text, size, color, aa=True, fonty="arial"):
    font = pygame.font.SysFont(fonty, size)
    textobj = font.render(text, aa, color)
    textrect = textobj.get_rect()
    return textobj, textrect


def drawText(text, xy):
    windowSurface.blit(text, xy)


def loadPicture(picture, xy=0):
    image = pygame.image.load("bilder\\%s" % picture).convert_alpha()
    rect = image.get_rect()
    if xy == 0:
        stretched = pygame.transform.scale(image, (rect.width, rect.height))
    else:
        stretched = pygame.transform.scale(image, xy)
        rect = stretched.get_rect()
    return (rect, stretched)


def drawPicture(picture, rectxy=(0, 0)):
    windowSurface.blit(picture, rectxy)


def loadBackground(picture):
    image = pygame.image.load("bilder\\%s" % picture).convert()
    rect = windowSurface.get_rect()
    stretched = pygame.transform.scale(image, (rect.width, rect.height))
    return stretched


def loadSound(sound):
    return pygame.mixer.Sound("music\\%s.wav" % sound)


def loadMusic(music):
    pygame.mixer.music.load("music\\%s.wav" % music)


def startMusic():
    pygame.mixer.music.play(-1, 0.0)


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def centerUp(rect, xy, x_only=False, y_only=False):
    if x_only:
        rect.left = xy[0] / 2 - rect.centerx
        rect.top = xy[1]
    elif y_only:
        rect.left = xy[0]
        rect.top = xy[1] / 2 - rect.centery
    else:
        rect.left = xy[0] / 2 - rect.centerx
        rect.top = xy[1] / 2 - rect.centery


def moveCursor(dic, list, number=False):  # cursor, list to iterate, amount of targets 1,3,6
    if not number or number == 1:
        if dic["leftclick"]:
            dic["pos"] -= 1
        if dic["rightclick"]:
            dic["pos"] += 1
        if dic["upclick"]:
            dic["pos"] = len(list) - 1
        if dic["downclick"]:
            dic["pos"] = 0

        if dic["pos"] < 0:
            dic["pos"] = 0
        if dic["pos"] >= len(list):
            dic["pos"] = len(list) - 1

    if dic["currentMenu"] in ("main", "skill"):
        if dic["upclick"]:
            dic["pos"] = len(list) - 1
        if dic["downclick"]:
            dic["pos"] = 0
        drawPicture(dic["picture"], [list[dic["pos"]][0] - 10, 610])
        drawPicture(dic["picture2"], [battleState["currentBattler"].position[0] - dic["rect2"].centerx,
                                      battleState["currentBattler"].position[1] -
                                      battleState["currentBattler"].rect.centery - 30])

    if dic["currentMenu"] == "target" and number == 6:
        for battler in list:
            drawPicture(dic["picture2"], [battler.position[0] - dic["rect2"].centerx,
                                          battler.position[1] - battler.rect.centery - 30])

    if dic["currentMenu"] == "target" and (number == 3 or number == 1):
        if dic["upclick"]:
            dic["targetteam"] = battleState["secondParty"]
            dic["pos"] = 0
        if dic["downclick"]:
            dic["targetteam"] = battleState["firstParty"]
            dic["pos"] = 0
        if number == 1:
            drawPicture(dic["picture2"], [list[dic["pos"]].position[0] - dic["rect2"].centerx,
                                          list[dic["pos"]].position[1] - list[dic["pos"]].rect.centery - 30])
        if number == 3:
            for battler in list:
                drawPicture(dic["picture2"], [battler.position[0] - dic["rect2"].centerx,
                                              battler.position[1] - battler.rect.centery - 30])

    dic["leftclick"] = False
    dic["rightclick"] = False
    dic["upclick"] = False
    dic["downclick"] = False
    dic["enterclick"] = False
    dic["backclick"] = False


def checkCommand(dic):  # cursor
    i = 0
    if dic["currentMenu"] == "main":
        for command in battleState["currentBattler"].commands:
            if dic["pos"] == i:
                battleState["currentBattler"].direction = command
                if battleState["currentBattler"].direction == "attack":
                    dic["targetteam"] = battleState["currentBattler"].enemyteam
                    dic["targetnumber"] = 1
            i += 1

    if dic["currentMenu"] == "target":
        if dic["targetnumber"] == 1:
            for target in dic["targetteam"]:
                if dic["pos"] == i:
                    if target.alive:
                        battleState["currentBattler"].target.append(target)
                        if battleState["currentBattler"].direction in ["skill", ]:
                            getNote("skill")
                    else:
                        getNumber(target.name, "dead", target)
                i += 1
        else:
            battleState["currentBattler"].target += dic["targetteam"]
            if battleState["currentBattler"].direction in ["skill", ]:
                            getNote("skill")

    if dic["currentMenu"] == "skill":
        for skill in battleState["currentBattler"].skills:
            if dic["pos"] == i:
                if checkAction(skill, battleState["currentBattler"]):
                    getTargetMarker(skill, battleState["currentBattler"])
                    battleState["currentBattler"].skillcommand = skill
                else:
                    getNumber(skill["name"], "no_stamina", battleState["currentBattler"])
            i += 1


def menuBackwards(dic):
    if dic["currentMenu"] == "main":
        pass

    if dic["currentMenu"] == "target":
        battleState["currentBattler"].direction = "idle"
        dic["pos"] = 0
        battleState["currentBattler"].skillcommand = False
        dic["currentMenu"] = "main"

    if dic["currentMenu"] == "skill":
        battleState["currentBattler"].direction = "idle"
        dic["pos"] = 0
        dic["currentMenu"] = "main"


def checkAction(action, battler):
    if action["actiontype"] == "skill":
        if battler.sp >= action["staminaUse"]:
            return True
        else:
            return False
    if action["actiontype"] == "attack":
        if battler.sp >= action["staminaUse"]:
            return True
        else:
            return False
    if action["actiontype"] == "item":
        return True
    else:
        return False


def getTargetMarker(action, battler):
    if action["targetteam"] == "ally":
        cursor["targetteam"] = battler.alliedteam
        if action["targetnumber"] == 1:
            cursor["targetnumber"] = 1
        if action["targetnumber"] == 3:
            cursor["targetnumber"] = 3
    if action["targetteam"] == "enemy":
        cursor["targetteam"] = battler.enemyteam
        if action["targetnumber"] == 1:
            cursor["targetnumber"] = 1
        if action["targetnumber"] == 3:
            cursor["targetnumber"] = 3
    if action["targetteam"] == "all":
        cursor["targetteam"] = battler.alliedteam + battler.enemyteam


def getNumber(text, typ, unit=None):
    if typ == "damage":
        numbers.append(
            {'text': "%s damage" % text, 'size': 40, 'position': [unit.position[0] + 40, unit.position[1] - 50],
             'color': WHITE, "timer": 0})
    if typ == "heal":
        numbers.append(
            {'text': "%s heal" % text, 'size': 40, 'position': [unit.position[0] + 40, unit.position[1] - 50],
             'color': GREEN, "timer": 0})
    if typ == "dead":
        numbers.append(
            {'text': "%s is dead!" % text, 'size': 20, 'position': [unit.position[0] + 40, unit.position[1] - 50],
             'color': RED, "timer": 0})
    if typ == "no_stamina":
        numbers.append(
            {'text': "No stamina for %s!" % text, 'size': 20,
             'position': [unit.position[0] + 40, unit.position[1] - 50],
             'color': RED, "timer": 0})


def getNote(type):  # type of notification as a string
    if type == "skill":
        color = BLACK
        skillname = battleState["currentBattler"].skillcommand["name"]
        textpic, textrect = loadText("%s" % skillname, 50, color)
        centerUp(textrect, [WINDOWWIDTH, 100], x_only=True)
        notes.append(
            {"pic": textpic, "rect": textrect, "timer": 0})


def drawNotification():
    global numbers
    for number in reversed(numbers):
        loadAndDrawText(number["text"], number["size"], number["position"], number["color"])
        number["position"][0] += 0.5
        number["position"][1] -= 0.5
        if number["timer"] >= 2400 / FPS:
            numbers.remove(number)
        else:
            number["timer"] += 60 / FPS

    for note in reversed(notes):
        pygame.draw.rect(windowSurface, WHITE, note["rect"])
        drawText(note["pic"], note["rect"])
        if note["timer"] >= 4800 / FPS:
            notes.remove(note)
        else:
            note["timer"] += 60 / FPS


def drawInterface(dic, dic3):  # cursor, battleState
    if dic["currentMenu"] != "target" and dic["currentMenu"]:
        if dic["currentMenu"] == "main":
            menulist = battleState["currentBattler"].commands
        if dic["currentMenu"] == "skill":
            menulist = dic3["currentBattler"].skills
        innerDistance = 20
        size = 80
        tiles = []
        outerDistance = (WINDOWWIDTH - ((len(menulist) * size) + ((len(menulist) - 1) * innerDistance))) / 2
        for i in range(0, len(menulist)):
            tiles.append(pygame.Rect(outerDistance + (i * (size + innerDistance)), 620, size, size))
            pygame.draw.rect(windowSurface, WHITE, tiles[i])
            if dic["currentMenu"] == "main":
                loadAndDrawText("%s" % menulist[i], 25, (outerDistance + (i * (size + innerDistance)), 620), RED)
            if dic["currentMenu"] == "skill":
                loadAndDrawText("%s" % menulist[i]["name"], 25, (outerDistance + (i * (size + innerDistance)), 620),
                                RED)
                loadAndDrawText("%s SP" % menulist[i]["staminaUse"], 25,
                                (outerDistance + (i * (size + innerDistance)), 650),
                                BLUE)
        moveCursor(dic, tiles)
        loadAndDrawText(dic3["currentBattler"].name, 40, [WINDOWWIDTH / 2 - 90, WINDOWHEIGHT - 150], BLACK)
    if dic["currentMenu"] == "target" and not dic3["currentBattler"].target:
        moveCursor(dic, dic["targetteam"], dic["targetnumber"])

    drawBattlerState(dic3)


def drawBattlerState(dic):  # battleState
    size = 15
    dist = 50
    disty = (WINDOWHEIGHT / 2) + 50
    distx = WINDOWWIDTH - 250
    i = 0

    #loadAndDrawText("%s" % dic["currentBattler"].target.name, 20, [WINDOWWIDTH/2, WINDOWHEIGHT/2], BLACK)
    for battler in dic["firstParty"]:
        loadAndDrawText("%s" % battler.name, size, [dist, dist + (i * 100)], BLACK)
        pygame.draw.rect(windowSurface, WHITE, (dist, dist + (size + 4) + (i * 100), 200, 10))
        if battler.alive:
            pygame.draw.rect(windowSurface, HPCOLOUR, (dist, dist + (size + 4) + (i * 100),
                                                       battler.getHP() * 200, 10))
            loadAndDrawText("%s / %s" % (battler.hp, battler.hpmax), size - 2, (dist + 80,
                                                                                dist + (size + 2) + (i * 100)), BLACK)
        else:
            loadAndDrawText("dead!", size - 2, (dist + 80, dist + (size + 2) + (i * 100)), HPCOLOUR)
        pygame.draw.rect(windowSurface, WHITE, (dist, dist + (size * 2) + (i * 100), 200, 8))
        pygame.draw.rect(windowSurface, STACOLOUR, (dist, dist + (size * 2) + (i * 100),
                                                    battler.getSP() * 200, 8))
        loadAndDrawText("SP: %s" % battler.sp, size - 4, (dist + 80, dist + (size * 2 - 2) + (i * 100)), BLACK)

        if battler.target:
            if len(battler.target) > 1:
                for target in battler.target:
                    targetname = ""
                    targetname += target.name
            else:
                targetname = battler.target[0].name
            loadAndDrawText("%s -> %s" % (battler.direction, targetname), size - 2,
                            [dist, dist + (size * 3 - 5) + (i * 100)],
                            BLACK)
        else:
            loadAndDrawText("%s" % battler.direction, size - 2, [dist, dist + (size * 3 - 5) + (i * 100)],
                            BLACK)
        loadAndDrawText("str %s, def %s, agi %s, pow %s" % (battler.strength, battler.defense, battler.agility,
                                                            battler.power), size - 5, [dist, dist + (size * 4 - 5)
                                                                                       + (i * 100)], BLACK)
        i += 1

    i = 0
    for battler in dic["secondParty"]:
        loadAndDrawText("%s" % battler.name, size, [distx, disty + (i * 100)], BLACK)
        pygame.draw.rect(windowSurface, WHITE, (distx, disty + (size + 4) + (i * 100), 200, 10))
        if battler.alive:
            pygame.draw.rect(windowSurface, HPCOLOUR, (distx, disty + (size + 4) + (i * 100),
                                                       battler.getHP() * 200, 10))
            loadAndDrawText("%s / %s" % (battler.hp, battler.hpmax), size - 2,
                            (distx + 80, disty + (size + 2) + (i * 100)),
                            BLACK)
        else:
            loadAndDrawText("dead!", size - 2, (distx + 80, disty + (size + 2) + (i * 100)), HPCOLOUR)
        pygame.draw.rect(windowSurface, WHITE, (distx, disty + (size * 2) + (i * 100), 200, 8))
        pygame.draw.rect(windowSurface, STACOLOUR, (distx, disty + (size * 2) + (i * 100),
                                                    battler.getSP() * 200, 8))
        loadAndDrawText("SP: %s" % battler.sp, size - 4, (distx + 80, disty + (size * 2 - 2) + (i * 100)), BLACK)

        if battler.target:
            if len(battler.target) > 1:
                for target in battler.target:
                    targetname = ""
                    targetname += target.name
            else:
                targetname = battler.target[0].name
            loadAndDrawText("%s -> %s" % (battler.direction, targetname), size - 2,
                            [distx, disty + (size * 3 - 5) + (i * 100)], BLACK)
        else:
            loadAndDrawText("%s" % battler.direction, size - 2, [distx, disty + (size * 3 - 5) + (i * 100)], BLACK)
        loadAndDrawText("str %s, def %s, agi %s, pow %s" % (battler.strength, battler.defense, battler.agility,
                                                            battler.power), size - 5, [distx, disty + (size * 4 - 5)
                                                                                       + (i * 100)], BLACK)
        i += 1


def drawBattler(dic):  # battleState
    for battler in dic["allBattler"]:
        battler.drawShadow()
    sorted_by_y = sorted(dic["allBattler"], key=lambda battler: battler.position[1])

    for battler in sorted_by_y:
        battler.draw()


def randomAllyTarget(dic):  # battleState
    while True:
        target = dic["firstParty"][random.randint(0, len(dic["firstParty"]) - 1)]
        if target.alive: return target


def randomEnemyTarget(dic):  # battleState
    while True:
        target = dic["secondParty"][random.randint(0, len(dic["secondParty"]) - 1)]
        if target.alive: return target


def getBattler(dic):  # battleState
    dic["firstParty"] = [figure(typ1), figure(typ2)]

    if random.randint(1, 100) > 20:

        for i in range(0, random.randint(1, 3)):
            dic["secondParty"].append(figure({
                "name": random.choice(names), "inventory": {}, "race": "human",
                "picture": random.choice(enemypictures),
                "strength": 5 + round(random.gauss(5, 2)),
                "defense": 4 + round(random.gauss(3, 2)),
                "agility": 4 + round(random.gauss(4, 2)),
                "power": 5 + round(random.gauss(5, 1)),
                "hitpoints": round(random.gauss(15, 6)),
                "stamina": round(random.gauss(5, 2)),
                "skills": [skill_heal],
                "commands": ["attack", "defend"],
                "status": [],
                "rect": [100, 93],
                "position": secondPartyPos[i],
                "POS": secondPartyPos[i]
            }))
            #dic["secondParty"][i].position = secondPartyPos[i]
            #dic["secondParty"][i].POS = secondPartyPos[i]
    else:
        dic["secondParty"].append(figure(boss))


def startBattle(dic):  # battleState
    dic["allBattler"].extend(dic["firstParty"])
    dic["allBattler"].extend(dic["secondParty"])
    dic["allBattler"].sort(key=attrgetter("agility"), reverse=True)  # backwards = highest first
    for battler in dic["allBattler"]:
        battler.getTeams()
    dic["turns"] = 0
    dic["rounds"] = 0
    dic["livingBattler"].extend(dic["firstParty"])  # ?
    dic["livingBattler"].extend(dic["secondParty"])  # ?
    dic["currentBattler"] = dic["allBattler"][dic["turns"]]
    cursor["targetteam"] = dic["secondParty"]
    if dic["currentBattler"] in dic["firstParty"]:
        cursor["currentMenu"] = "main"
    else:
        cursor["currentMenu"] = False


def nextRound(dic):  # battleState
    dic["allBattler"].sort(key=attrgetter("agility"), reverse=True)
    dic["turns"] = 0
    dic["rounds"] += 1
    dic["currentBattler"] = dic["allBattler"][dic["turns"]]
    if dic["currentBattler"] in dic["firstParty"]:
        cursor["currentMenu"] = "main"
    for battler in dic["allBattler"]:
        if battler.alive:
            battler.direction = "idle"
            battler.target = []


def battleProcess(dic, dic2):  # battleState, cursor
    if dic["currentBattler"].direction in ("stop", "defend", "flee") or not dic["currentBattler"].alive:
        if dic["currentBattler"].direction == "flee":
            dic["allBattler"].remove(dic["currentBattler"])
            dic["firstParty"].remove(dic["currentBattler"])
        dic2["pos"] = 0
        dic2["targetteam"] = dic["secondParty"]
        dic2["targetnumber"] = False
        dic["currentBattler"].target = []
        dic["currentBattler"].skillcommand = False
        if dic["FiPaDead"] or dic["SePaDead"]:
            battleOver(dic)
        if dic["turns"] < len(dic["allBattler"]) - 1:
            dic["turns"] += 1
            dic["currentBattler"] = dic["allBattler"][dic["turns"]]
            #while not dic["currentBattler"].alive:
            #    dic["turns"] += 1
            #    dic["currentBattler"] = dic["allBattler"][dic["turns"]]
            dic2["targetteam"] = dic["secondParty"]
            if dic["currentBattler"] in dic["firstParty"] and dic["currentBattler"].alive:
                dic2["currentMenu"] = "main"
            if dic["currentBattler"] in dic["secondParty"]:
                dic2["currentMenu"] = False
        else:
            nextRound(dic)

    if dic["currentBattler"] in dic["firstParty"]:
        if not dic["currentBattler"].target:
            if dic["currentBattler"].direction == "attack":
                dic2["currentMenu"] = "target"
            if dic["currentBattler"].direction == "skill":
                dic2["currentMenu"] = "skill"
                if dic["currentBattler"].skillcommand:
                    dic2["currentMenu"] = "target"
            if dic["currentBattler"].direction == "flee":
                dic["allBattler"].remove(dic["currentBattler"])
                battleOver(dic)
        if dic["currentBattler"].target:
            dic["currentBattler"].execution(dic["currentBattler"].target)

    if dic["currentBattler"] in dic["secondParty"] and dic["currentBattler"].alive:
        if dic["currentBattler"].direction == "idle" and not dic["currentBattler"].target:
            if not dic["currentBattler"].target:
                for skill in dic["currentBattler"].skills:
                    if dic["currentBattler"].checkSkillCondition(skill):
                        break
            if not dic["currentBattler"].target:
                chance = random.randint(1, 100)
                if chance > 30:
                    dic["currentBattler"].direction = "attack"
                else:
                    dic["currentBattler"].direction = "defend"
                # dic["currentBattler"].randomCommand(dic["currentBattler"].commands)
                if dic["currentBattler"].direction == "attack":
                    dic["currentBattler"].target.append(randomAllyTarget(dic))
        if dic["currentBattler"].target:
            dic["currentBattler"].execution(dic["currentBattler"].target)


def checkBattlerCondition(dic):  # battleState
    firstpartydead = 0
    secondpartydead = 0

    for battler in dic["allBattler"]:
        if battler.hp <= 0:
            battler.hp = 0
            battler.alive = False
        if battler.hp > battler.hpmax:
            battler.hp = battler.hpmax
        if battler.sp > battler.spmax:
            battler.sp = battler.spmax
        if battler.sp < 0:
            battler.sp = 0
        if battler.direction in ("stop", "attack", "skill", "idle") and battler.alive:
            if battler.z >= 20:
                battler.zdir = -15 / FPS
            if battler.z <= 0:
                battler.zdir = 15 / FPS
            battler.z += battler.zdir
        if battler.direction in ("defense",) and battler.alive:
            battler.z = 5
        if not battler.alive:
            battler.z = 0

    for battler in dic["firstParty"]:
        if battler.hp <= 0:
            battler.alive = False
            firstpartydead += 1

    for battler in dic["secondParty"]:
        if battler.hp <= 0:
            battler.alive = False
            secondpartydead += 1

    if firstpartydead == len(dic["firstParty"]):
        dic["FiPaDead"] = True
    if secondpartydead == len(dic["secondParty"]):
        dic["SePaDead"] = True


def battleOver(dic):  # battleState
    time.sleep(2)
    windowSurface.fill(BLACK)
    if dic["FiPaDead"]:
        text, rect = loadText("YOU SUCK", 100, WHITE)
        centerUp(rect, [WINDOWWIDTH, WINDOWHEIGHT])
        drawText(text, rect)
    elif dic["SePaDead"]:
        text, rect = loadText("YOU DOMINATE", 100, WHITE)
        centerUp(rect, [WINDOWWIDTH, WINDOWHEIGHT])
        drawText(text, rect)
    else:
        text, rect = loadText("YOU RAN FROM LIFE", 100, WHITE)
        centerUp(rect, [WINDOWWIDTH, WINDOWHEIGHT])
        drawText(text, rect)
    pygame.display.flip()
    waitForPlayerToPressKey()
    terminate()


"""class number:
    def __init__(self, xy):
        self.counter = 0
        self.position = xy
        numbers.append(self)

    def draw(self, number, typ, unit):
        self.counter += 1
        self.position[0] -= 1
        if typ == "damage":
            drawText("%s" % number, 20,
                     (unit.position[0] + (unit.rect.width / 2) + self.counter, unit.position[1] + self.counter), WHITE)
        if typ == "heal":
            drawText("%s" % number, 20,
                     (unit.position[0] + (unit.rect.width / 2) + self.counter, unit.position[1] + self.counter), GREEN)
 NUTZLOS"""


class figure:
    """ erstellt jegliche auch kampffähige figuren """

    def __init__(self, dic):  # figurendictionary
        self.name = dic["name"]
        self.inventory = dic["inventory"]
        self.equip = {"head": False,
                      "body": False,
                      "lhand": False,
                      "rhand": False,
                      "ornament": False}
        self.atomicpower = False,
        self.race = dic["race"]
        self.level = 1
        self.exp = 0
        self.alive = True

        self.strength = dic["strength"]
        self.defense = dic["defense"]
        self.agility = dic["agility"]
        self.power = dic["power"]
        self.hp = dic["hitpoints"]
        self.hpmax = dic["hitpoints"]
        self.sp = dic["stamina"]
        self.spmax = dic["stamina"]
        self.skills = dic["skills"]
        self.commands = dic["commands"]
        self.status = dic["status"]

        self.position = dic["position"]
        self.z = 0
        self.zdir = 1
        self.rect, self.picture = loadPicture(dic["picture"], dic["rect"])
        self.POS = dic["position"][0],dic["position"][1] + self.rect.centery
        self.shadowrect, self.shadow = loadPicture("shadow2.png",
                                                   (round(self.rect.width / 3 * 2), round(self.rect.height / 5)))
        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False
        self.direction = "idle"
        self.speed = 20
        self.phase = 1
        self.target = []
        self.alliedteam = False
        self.enemyteam = False
        self.skillcommand = False
        figures.append(self)

    def draw(self):
        drawPicture(self.picture, [self.position[0] - self.rect.centerx,
                                   (self.position[1] - self.rect.centery) - self.z])

    def drawShadow(self):
        drawPicture(self.shadow,
                    [self.position[0] - self.shadowrect.centerx, self.position[1] + self.rect.height * 0.35])

    def getTeams(self):
        if self in battleState["firstParty"]:
            self.alliedteam = battleState["firstParty"]
            self.enemyteam = battleState["secondParty"]

        if self in battleState["secondParty"]:
            self.alliedteam = battleState["secondParty"]
            self.enemyteam = battleState["firstParty"]


    def move(self):
        if self.moveDown and self.position[1] < WINDOWHEIGHT:
            self.position[1] += MOVESPEED
        if self.moveUp and self.position[1] > 0:
            self.position[1] -= MOVESPEED
        if self.moveLeft and self.position[0] > 0:
            self.position[0] -= MOVESPEED
        if self.moveRight and self.position[0] < WINDOWWIDTH:
            self.position[0] += MOVESPEED

    def moveToTarget(self, target=False):
        if self.phase == 1:
            if self.skillcommand and (self.skillcommand["targetnumber"] == 3 or self.skillcommand["targetnumber"] == 6):
                targetx, targety = windowSurface.get_rect().center
            else:
                targetx, targety = [self.target[0].position[0], self.target[0].position[1] + self.target[0].rect.centery]
        if self.phase == 3:
            targetx, targety = self.POS
        speed = FPS * 0.5
        selfx, selfy = self.position[0], self.position[1] + self.rect.centery
        direction = [round(targetx - selfx), round(targety - selfy)]
        distance = math.sqrt(((direction[0]) ** 2) + ((direction[1]) ** 2))
        # V1 geschmeidig
        factor = [direction[0] / speed, direction[1] / speed]
        self.position = [self.position[0] + factor[0], self.position[1] + factor[1]]
        # V2 steif
        # total = abs(direction[0]) + abs(direction[1])
        # factor = [direction[0] / total, direction[1] / total]
        # self.position = [self.position[0] + (self.speed * factor[0]), self.position[1] + (self.speed * factor[1])]
        if self.phase == 1 and (self.rect.height / 2) > distance < (self.rect.width / 2):
            self.phase = 2
        if self.phase == 3 and abs(selfx - self.POS[0]) < 20 > abs(selfy - self.POS[1]):
            self.phase = 1
            self.direction = "stop"


    def attackTarget(self, target):
        if self.target[0].direction == "defend":
            damage = round(self.strength - target[0].defense)
        else:
            damage = round(self.strength - (target[0].defense / 2))
        if damage < 0:
            damage = 0
        type = "damage"
        getNumber(damage, type, target[0])
        target[0].hp -= damage
        self.phase = 3

    def useSkill(self, target):
        name = self.skillcommand["name"]
        staminaUse = self.skillcommand["staminaUse"]
        skilltype = self.skillcommand["type"]
        damagetype = self.skillcommand["damagetype"]
        healtype = self.skillcommand["healtype"]
        bufftype = self.skillcommand["bufftype"]
        amount = self.skillcommand["amount"]
        properties = self.skillcommand["properties"]
        factor = self.skillcommand["factor"]
        attribute = attrgetter(self.skillcommand["attribute"])(self)
        properties = self.skillcommand["properties"]
        targetteam = self.skillcommand["targetteam"]
        targetnumber = self.skillcommand["targetnumber"]

        amount = round(amount + (factor * attribute))

        if "drain_self_sp" in properties:
            self.sp -= amount

        for targets in self.target:
            #amount = round(amount + (factor * attribute))

            if skilltype == "damage":
                if damagetype == "physical":
                    if "physical_penetration" in properties:
                        pass
                    elif targets.direction == "defense":
                        amount -= round(targets.defense)
                    else:
                        amount -= round(targets.defense / 2)
                if damagetype == "magical":
                    amount -= round(targets.power / 3)

            if amount < 0:
                amount = 0

            getNumber(amount, skilltype, targets)
            if skilltype == "heal":
                if healtype == "hp":
                    targets.hp += amount
                if healtype == "sp":
                    targets.sp += amount
            if skilltype == "damage":
                if damagetype == "drain":
                    targets.hp -= amount
                    self.hp += round(amount/2)
                    getNumber(round(amount/2), "heal", self)
                else:
                    targets.hp -= amount
            if skilltype == "buff":
                if bufftype == "strength":
                    targets.strength += amount
                if bufftype == "defense":
                    targets.defense += amount
                if bufftype == "hpregen":
                    targets.status += ["hpregen", self.hpmax, factor]  # name, attribute, value
        self.sp -= staminaUse
        #if targetnumber == 3:
        #    for battler in self.target:
        #        getNumber(amount, skilltype, target)


        self.phase = 3

    def execution(self, target):
        if self.direction == "attack":
            self.attackCommand(target)
        if self.direction == "defend":
            self.direction = "defend"
        if self.direction == "skill":
            self.skillCommand(target)
        if self.direction == "items":
            time.sleep(0.5)
            self.direction = "stop"
            # if self.direction == "flee":
            # battleState["firstParty"].remove(self)

    def randomCommand(self, commands):  # commands
        self.direction = random.choice(commands)

    def getSkillCommand(self, skill, target):
        self.skillcommand = skill
        self.direction = "skill"
        self.target += target
        getNote("skill")

    def checkSkillNeeded(self, list, skill, damagetype=False, healtype=False, bufftype=False, properties=False):
        if not list:
            return False

        if len(list) == 1:
            if skill["targetnumber"] == 1:
                self.getSkillCommand(skill, [list[0]])
                return True
            if self.gotAnotherSkill("damage", 3, damagetype, healtype, bufftype, properties):
                return False
            else:
                self.getSkillCommand(skill, [list])
                return True

        if len(list) > 1:
            if skill["targetnumber"] == 3:
                self.getSkillCommand(skill, list)
                return True
            if self.gotAnotherSkill("damage", 1, damagetype, healtype, bufftype, properties):
                return False
            else:
                self.getSkillCommand(skill, [list[0]])
                return True

    def checkSkillCondition(self, skill):
        if self.sp < skill["staminaUse"]:
            return False

        if skill["targetnumber"] == 6:
            if self.getHP() < 0.1:
                self.getSkillCommand(skill, self.alliedteam + self.enemyteam)
                return True
            else:
                return False

        if skill["type"] == "damage" and "physical" in skill["damagetype"]:
            validtargets = []
            if not skill["properties"]:
                for battler in self.enemyteam:
                    if battler.direction == "defend" and battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("hp"))
                if self.checkSkillNeeded(validtargets, skill, damagetype="physical"):
                    return True
                else:
                    return False

            if "physical_penetration" in skill["properties"]:
                for battler in self.enemyteam:
                    if battler.direction == "defend" and battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("hp"))
                if self.checkSkillNeeded(validtargets, skill, damagetype="physical",
                                         properties="physical_penetration"):
                    return True
                else:
                    return False

        if skill["type"] == "damage" and "magical" in skill["damagetype"]:
            validtargets = []
            if not skill["properties"]:
                for battler in self.enemyteam:
                    if battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("hp"))
                if self.checkSkillNeeded(validtargets, skill, damagetype="magical"):
                    return True
                else:
                    return False

        if skill["type"] == "damage" and "pure" in skill["damagetype"]:
            validtargets = []
            if not skill["properties"]:
                for battler in self.enemyteam:
                    if battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("hp"))
                if self.checkSkillNeeded(validtargets, skill, damagetype="pure"):
                    return True
                else:
                    return False

        if skill["type"] == "damage" and "drain" in skill["damagetype"]:
            validtargets = []
            if "drain_hp" in skill["properties"]:
                for battler in self.enemyteam:
                    if battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("hp"))
                if self.checkSkillNeeded(validtargets, skill, damagetype="drain", properties="drainhp"):
                    return True
                else:
                    return False

            if "drain_sp" in skill["properties"]:
                for battler in self.enemyteam:
                    if battler.alive:
                        validtargets.append(battler)
                validtargets.sort(key=attrgetter("sp"), reverse=True)
                if self.checkSkillNeeded(validtargets, skill, damagetype="drain", properties="drainsp"):
                    return True
                else:
                    return False

        if skill["type"] == "heal" and "hp" in skill["healtype"]:
            neededheal = []
            for battler in self.alliedteam:
                if battler.getHP() < 0.3 and battler.alive:
                    neededheal.append(battler)
            neededheal.sort(key=attrgetter("hp"))
            if self.checkSkillNeeded(neededheal, skill, healtype="hp"):
                return True
            else:
                return False

        if skill["type"] == "heal" and "sp" in skill["healtype"]:
            neededheal = []
            for battler in self.alliedteam:
                if battler.getSP() < 0.3 and battler.alive:
                    neededheal.append(battler)
            neededheal.sort(key=attrgetter("sp"))
            if self.checkSkillNeeded(neededheal, skill, healtype="sp"):
                return True
            else:
                return False

        if skill["type"] == "heal" and "poison" in skill["healtype"]:
            neededheal = []
            for battler in self.alliedteam:
                if "poison" in battler.status and battler.alive:
                    neededheal.append(battler)
            neededheal.sort(key=attrgetter("hp"), reverse=True)
            if self.checkSkillNeeded(neededheal, skill, healtype="poison"):
                return True
            else:
                return False

        if skill["type"] == "buff" and "strength" in skill["bufftype"]:
            neededbuff = []
            for battler in self.alliedteam:
                if battler.alive:
                    neededbuff.append(battler)
            neededbuff.sort(key=attrgetter("strength"), reverse=True)
            if self.checkSkillNeeded(neededbuff, skill, bufftype="strength"):
                return True
            else:
                return False

        if skill["type"] == "buff" and "defense" in skill["bufftype"]:
            neededbuff = []
            for battler in self.alliedteam:
                if battler.alive:
                    neededbuff.append(battler)
            neededbuff.sort(key=attrgetter("defense"))
            if self.checkSkillNeeded(neededbuff, skill, bufftype="defense"):
                return True
            else:
                return False

        if skill["type"] == "buff" and "hpregen" in skill["bufftype"]:
            neededbuff = []
            for battler in self.alliedteam:
                if battler.alive:
                    neededbuff.append(battler)
            neededbuff.sort(key=attrgetter("hpmax"), reverse=True)
            if self.checkSkillNeeded(neededbuff, skill, bufftype="hpregen"):
                return True
            else:
                return False

        return False


    def gotAnotherSkill(self, type, target, damagetype=False, healtype=False, bufftype=False, properties=False):
        list = []
        for skill in self.skills:
            if skill["properties"] == properties:
                if damagetype:
                    if skill["type"] == type and skill["targetnumber"] == target and skill["damagetype"] == damagetype:
                        list.append(skill)
                if healtype:
                    if skill["type"] == type and skill["targetnumber"] == target and skill["healtype"] == healtype:
                        list.append(skill)
                if bufftype:
                    if skill["type"] == type and skill["targetnumber"] == target and skill["bufftype"] == bufftype:
                        list.append(skill)
        if list:
            return True
        else:
            return False


    def attackCommand(self, target):
        if self.phase == 1:
            self.moveToTarget(target)
        if self.phase == 2:
            self.attackTarget(target)
        if self.phase == 3:
            self.moveToTarget()

    def skillCommand(self, target):
        if self.phase == 1:
            self.moveToTarget(target)
        if self.phase == 2:
            self.useSkill(target)
        if self.phase == 3:
            self.moveToTarget()

    def getHP(self):
        if self.hpmax <= 0:
            self.alive = False
        if self.alive:
            factor = self.hp / self.hpmax
        else:
            factor = 0
        return factor

    def getSP(self):
        if self.spmax <= 0:
            return 0
        else:
            factor = self.sp / self.spmax
            return factor

    def ValidSkillCommand(self, skill, target):
        if self.sp >= skill["staminaUse"] and target.alive:
            return True
        else:
            return False


# ENDE
