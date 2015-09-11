
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

chanceDistr = 1/10
blankTileChance = 0.01

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
    attrList = [whiteAttr, blackAttr]

    if invasiveBlackEnabled is not 0:
        attrList.append(blackIAttr)

    if invasiveWhiteEnabled is not 0:
        attrList.append(whiteIAttr)



def setInvasiveBlackTemp(temp):
    blackIAttr[-1] = temp

def setInvasiveWhiteTemp(temp):
    whiteIAttr[-1] = temp

def createDaisy(tile):
    global world
    if world is None:
        return None

    # figure out what daisy to spawn, return it.
    # if by chance no daisy spawns, return None

    # get adjacent tiles
    adj = []
    for x in range(-1,2):
        for y in range(-1,2):
            if(x != y and y != 0):
                    adj.append(world.getTile((tile.coords[0]+x,
                                             tile.coords[1]+y)))

    # shuffle list so no bias
    random.shuffle(adj)

    # try spawning off each tile
    for t in adj:
        if(t.obj is not None):
            if random.random() < 1-chanceDistr*abs(t.temp -
                                                   t.obj.optTemp):
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
                # attempt to spawn daisy based on difference in temp.
                if random.random() < 1-chanceDistr*abs(tile.temp -
                                                       attrList[0][-1]):

                    # spawn random type of daisy
                    return Daisy(t,attrList[0][0],
                                 attrList[0][1])
    return None
