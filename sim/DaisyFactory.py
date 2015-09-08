
import random

world = None

invasiveBlackEnabled = 0
invasiveWhiteEnabled = 0

whiteAttr = [0.75, 22.5]
blackAttr = [0.25, 22.5]
whiteIAttr = [0.75, 12.5]
blackIAttr = [0.25, 32.5]

# This feels bad...
def setWorld(w):
    world = w

def setInvasiveBlack(state):
    invasiveBlackEnabled = state

def setInvasiveWhite(state):
    invasiveWhiteEnabled = state

def setInvasiveBlackTemp(temp):
    blackIAttr[-1] = temp

def setInvasiveWhiteTemp(temp):
    whiteIAttr[-1] = temp

def createDaisy(currentTemp, xTileCoord, yTileCoord):
    # figure out what daisy to spawn, return it.
    # if by chance no daisy spawns, return None
    chance = random.random()
