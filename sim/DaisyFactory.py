
import random
from Daisy import Daisy

world = None

invasiveBlackEnabled = 0
invasiveWhiteEnabled = 0

whiteAttr = [0.75, 22.5]
blackAttr = [0.25, 22.5]
whiteIAttr = [0.25, 12.5]
blackIAttr = [0.75, 32.5]

# there should be a better way to do this, but this should be good
# enough for now
attrList = [whiteAttr, blackAttr]

chanceDistr = 1/17
blankTileChance = 0.05

minTemp = 0
maxTemp = 0

# This feels bad...
def setWorld(w):
    global world
    world = w

def setInvasiveBlack(state):
    global invasiveBlackEnabled
    invasiveBlackEnabled = state
    updateAttr()

def setInvasiveWhite(state):
    global invasiveWhiteEnabled
    invasiveWhiteEnabled = state
    updateAttr()

def updateAttr():
    global invasiveBlackEnabled
    global invasiveWhiteEnabled
    global attrList
    global minTemp
    global maxTemp
    attrList = [whiteAttr, blackAttr]

    if invasiveBlackEnabled is not 0:
        attrList.append(blackIAttr)

    if invasiveWhiteEnabled is not 0:
        attrList.append(whiteIAttr)

    minTemp = min([a[-1]-17.5 for a in attrList])
    maxTemp = max([a[-1]+17.5 for a in attrList])


def setInvasiveBlackTemp(temp):
    blackIAttr[-1] = temp

def setInvasiveWhiteTemp(temp):
    whiteIAttr[-1] = temp

def createDaisy(tile):
    global world
    global minTemp
    global maxTemp
    # either no world yet or cannot even hope to spawn new daisies here.
    if world is None or tile.temp < minTemp or tile.temp > maxTemp:
        return None

    # figure out what daisy to spawn, return it.
    # if by chance no daisy spawns, return None

    # get adjacent tiles
    adj = [world.getTile((tile.coords[0]+x, tile.coords[1]+y))
           for x in range(-1,2)
           for y in range(-1,2)
           if (x != y and y != 0)]

    # shuffle list so no bias
    random.shuffle(adj)

    # try spawning off each tile
    for t in adj:
        if(t.obj is not None):
            chance = 0.0032625*(t.obj.optTemp - tile.temp)**2
            if random.random() > chance:
                # spawn this type of daisy
                return Daisy(t, t.obj.albedo,
                             t.obj.optTemp)


        else:
            # current object is blank!

            # 1% chance to spawn daisy off
            # blank tile
            if random.random() < blankTileChance:
                # yes, I know shuffle is done in place. Doesn't
                # matter for this application
                random.shuffle(attrList)
                chance = 0.0032625*(attrList[0][1] - tile.temp)**2
                # attempt to spawn daisy based on difference in temp.
                if random.random() > chance:
                    # spawn random type of daisy
                    return Daisy(t,attrList[0][0],
                                 attrList[0][1])
    return None
