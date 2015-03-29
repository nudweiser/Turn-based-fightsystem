import random, time, pygame, sys

from machine import firstPartyPos, secondPartyPos

battleState = {
    "allBattler": [],
    "livingBattler": [],
    "firstParty": [],
    "secondParty": [],
    "FiPaDead": False,
    "SePaDead": False,
    "currentBattler": None,
    "turns": 0,
    "rounds": 0
}

"""commands = [
    "attack",
    "defend",
    "skill",
    "items",
    "flee"
]"""

cursor = {
    "picture": None,
    "rect": [],
    "picture2": None,
    "rect2": [],
    "position": [390, 610],
    "pos": 0,
    "leftclick": False,
    "rightclick": False,
    "upclick": False,
    "downclick": False,
    "enterclick": False,
    "backclick": False,
    "active": False,
    "currentMenu": "main",
    "targetteam": False,  # alliedteam, enemyteam, all
    "targetnumber": False  # 1, 3, 6
}

names = "Abo Achim Adolf Albrecht Alexander Alois Ambros Andreas Anselm Anton Armin Arndt Arno Arnold Arnulf Axel \
        Augustus Axel Benjamin Bernd Bernhard Berthold Bodo Bruno Carsten Christian Christof Klemens Konrad Kurt \
        Dagobert Detlef Detlev Dieter Dietrich Dierk Dirk Dolf Dominik Egon Elias Elmar Emil Emmerich Engelbert \
        Erhard Erich Erik Ernst Erwin Eugen Ewald Fabian Falco Felix Ferdinand Florian Franz Friedhelm Friedrich \
        Fritz Gebhard Georg Gerhard Gernot Golo Gottfried Gotthold Gottlieb Gregor Günther Gustaf Hans Hannes Harald \
        Hartmut Hartwig Heiner Heinrich Heinz Helge Helmut Herbert Hildebrand Holger Horst Hugbert Hugo Ignaz Ingemar \
        Jan Jens Joachim Achim Johann Johannes Jonas Jörg Jürgen Kai Karl Karlheinz Karsten Kaspar Klaus Knut Kristian \
        Kristof Lars Laurenz Lenz Leon Leonhard Leopold Lothar Ludwig Lukas Luther Lutz Manfred Marcel Marko Mario \
        Marius Markus Martin Matthäus Matthias Max Maximilian Meinhard Michael Nikolaus Nils Norbert Olof Oskar Oswald \
        Oswin Otto Philipp Poldi Raimund Rainer Ralf Randolf Reinhard Reinhold René Richard Rüdiger Rudolf Rupert \
        Sabine Schorsch Sebastian Joseph Simon Stefan Steffen Sven Theodor Thomas Till Tim Tobias Torsten Udo Ulf \
        Ulrich Urban Urs Uwe Veit Viktor Vinzenz Volkard Volker Waldemar Walther Wendel Wenzel Werner Wilfried Wilhelm \
        Wolfgang Wolfram".split()

enemypictures = "cat.png face80s.png hallosur4er.png pog.png" \
                " rider.png sam.png travolta.png weinbrandt.png fiji.png".split()

#SKILLS

skill_heal = {
    "name": "Heal",  # name?!
    "actiontype": "skill",  # skill, attack, item, move
    "staminaUse": 4,  # how much stamina used
    "amount": 10,  # value of the skill
    "type": "heal",  # damage, heal, buff, debuff
    "damagetype": "magical",  # physical, magical, pure, drain
    "healtype": "hp",  # hp, mana, statuseffects
    "bufftype": False,  # attribute, aura, buff, regen
    "properties": [],  # list of side effect/s, like physical_penetration
    "factor": 0.25,  # how much the attribute changes the value
    "attribute": "power",  # battler.attribute
    "targetteam": "ally",  # ally , enemy, all
    "targetnumber": 1,  # amounts of targets, 1 for single, 3 for full team
}

skill_share = {
    "name": "Share",
    "actiontype": "skill",
    "staminaUse": 0,
    "amount": 0,
    "type": "heal",
    "damagetype": False,
    "healtype": "sp",
    "bufftype": False,
    "properties": ["drain_self_sp"],
    "factor": 0.50,
    "attribute": "sp",
    "targetteam": "ally",
    "targetnumber": 1,
}

skill_bash = {
    "name": "Bash",
    "actiontype": "skill",
    "staminaUse": 3,
    "amount": 5,
    "type": "damage",
    "damagetype": "physical",
    "healtype": False,
    "bufftype": False,
    "properties": ["physical_penetration"],
    "factor": 0.25,
    "attribute": "strength",
    "targetteam": "enemy",
    "targetnumber": 1,
}

skill_cleave = {
    "name": "Cleave",
    "actiontype": "skill",
    "staminaUse": 5,
    "amount": 5,
    "type": "damage",
    "damagetype": "physical",
    "healtype": False,
    "bufftype": False,
    "properties": [],
    "factor": 0.25,
    "attribute": "strength",
    "targetteam": "enemy",
    "targetnumber": 3,
}

#BATTLER

typ1 = {
    'name': "Fiji Konde", 'inventory': {}, 'race': "human",
    'picture': "chin.png",
    'strength': 7 + round(random.gauss(5, 5)),
    'defense': 4 + round(random.gauss(3, 1)),
    'agility': 6 + round(random.gauss(5, 3)),
    'power': 1 + round(random.gauss(2, 4)),
    'hitpoints': round(random.gauss(18, 6)),
    'stamina': 5 + round(random.gauss(5, 2)),
    "skills": [skill_bash, skill_cleave],
    "commands": ["attack", "defend", "skill", "items", "flee"],
    "status": [],
    'rect': [120, 120],
    'position': firstPartyPos[0]
}

typ2 = {
    "name": "Kleiner Spacki", "inventory": {}, "race": "human",
    "picture": "spacki.png",
    "strength": 4 + round(random.gauss(4, 1)),
    "defense": 6 + round(random.gauss(5, 3)),
    "agility": 4 + round(random.gauss(4, 2)),
    "power": 5 + round(random.gauss(5, 1)),
    "hitpoints": round(random.gauss(24, 5)),
    "stamina": 5 + round(random.gauss(5, 2)),
    "skills": [skill_heal, skill_share],
    "commands": ["attack", "defend", "skill", "items", "flee"],
    "status": [],
    "rect": [120, 120],
    "position": firstPartyPos[1]
}

enemy = {
    "name": random.choice(names), "inventory": {}, "race": "human",
    "picture": "figur4.png",
    "strength": 5 + round(random.gauss(5, 2)),
    "defense": 4 + round(random.gauss(3, 2)),
    "agility": 4 + round(random.gauss(4, 2)),
    "power": 5 + round(random.gauss(5, 1)),
    "hitpoints": round(random.gauss(15, 6)),
    "stamina": 5 + round(random.gauss(5, 2)),
    "skills": False,
    "commands": ["attack", "defense"],
    "status": [],
    "rect": [100, 130],
    "position": []
}

boss = {
    "name": "Der Chatman", "inventory": {}, "race": "human",
    "picture": random.choice(enemypictures),   # "figur3.png",
    "strength": 6 + round(random.gauss(5, 1)),
    "defense": 7 + round(random.gauss(5, 3)),
    "agility": 3 + round(random.gauss(4, 1)),
    "power": 10 + round(random.gauss(7, 3)),
    "hitpoints": 10 + round(random.gauss(30, 8)),
    "stamina": 4 + round(random.gauss(10, 4)),
    "skills": [skill_bash, skill_heal],  # enemy skill priority from left to right
    "commands": ["attack", "defend"],
    "status": [],
    "rect": [320, 320],
    "position": secondPartyPos[1]
}
