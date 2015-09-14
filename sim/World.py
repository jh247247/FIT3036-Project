import sys, random
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Tile import Tile
from Sun import Sun
import DaisyFactory

class World(QWidget):
    SIZE_X = 35
    SIZE_Y = 35
    START_TEMP = 22.5
    def __init__(self, sun):
        super().__init__()

        self.sun = sun
        self.tick = 0

        # calculate start temp from sun
        self.avgTemp = self.START_TEMP
        # TODO: variation dependent on the position of the tile?
        self.worldTiles = [[Tile(self, World.START_TEMP, (x,y)) \
                            for x in range(self.SIZE_X)] \
                           for y in range(self.SIZE_Y)]
        self.worldLock = threading.Lock()

        self.initOptionsUI()
        DaisyFactory.setWorld(self)

        self.update()

    def initOptionsUI(self):
        self.avgTempLabel = QLabel("Average temp: " + str(self.START_TEMP))
        self.enableInvasiveBlack = QCheckBox("Enable invasive black")
        self.enableInvasiveBlack.stateChanged.connect(DaisyFactory.setInvasiveBlack)

        self.enableInvasiveWhite = QCheckBox("Enable invasive white")
        self.enableInvasiveWhite.stateChanged.connect(DaisyFactory.setInvasiveWhite)

        self.invasiveBlackTemp = QDoubleSpinBox()
        self.invasiveBlackTemp.valueChanged.connect(DaisyFactory.setInvasiveBlackTemp)
        self.invasiveBlackTemp.setValue(32.5) # TODO: not hardcode defaults

        self.invasiveWhiteTemp = QDoubleSpinBox()
        self.invasiveWhiteTemp.valueChanged.connect(DaisyFactory.setInvasiveWhiteTemp)
        self.invasiveWhiteTemp.setValue(12.5) # TODO: not hardcode defaults

        self.resetButton = QPushButton("Reset Simulation")
        self.resetButton.released.connect(self.resetWorld)

    def resetWorld(self):
        self.worldLock.acquire()
        self.worldTiles = [[Tile(self, World.START_TEMP, (x,y)) \
                            for x in range(self.SIZE_X)] \
                           for y in range(self.SIZE_Y)]
        self.worldLock.release()

        self.tick = 0


    def updateOptionsUI(self):
        self.avgTempLabel.setText("Average temp: " + str(round(self.avgTemp,4)))

    def update(self):
        self.worldLock.acquire()


        self.tick += 1

        tempTileArr = []

        # let the tiles update their temps
        for i in range(self.SIZE_X):
            tempTileArr.extend(self.worldTiles[i])

        random.shuffle(tempTileArr)
        for t in tempTileArr:
            t.update(self.sun.radiation)


        deltaTempTiles = [[0 for x in range(self.SIZE_X)] \
                           for y in range(self.SIZE_Y)]


        # let adjacent tiles affect one another
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                deltaTempTiles[i][j] += self.worldTiles[i][j].temp - \
                                  self.worldTiles[i-1][j].temp
                deltaTempTiles[i][j] += self.worldTiles[i][j].temp - \
                                  self.worldTiles[i][j-1].temp
                deltaTempTiles[i][j] += self.worldTiles[i][j].temp - \
                                        self.worldTiles[(i+1)%self.SIZE_X][j].temp
                deltaTempTiles[i][j] += self.worldTiles[i][j].temp - \
                                        self.worldTiles[i][(j+1)%self.SIZE_Y].temp
                deltaTempTiles[i][j] /= 4 # TODO: fix factor...
                deltaTempTiles[i][j] *= 0.2

        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].temp -= deltaTempTiles[i][j]

        self.avgTemp = 0
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.avgTemp += self.worldTiles[i][j].temp

        self.worldLock.release()
        self.avgTemp /= self.SIZE_X*self.SIZE_Y
        self.sun.update()
        print(str(self.avgTemp) + " , " + str(self.sun.radiation) + \
              " , "+ str(self.tick))

        self.updateOptionsUI()

        threading.Timer(0.001,self.update).start()


    def draw(self, qp):
        size = self.size()
        incX = size.width()/self.SIZE_X
        incY = size.height()/self.SIZE_Y


        # let the tiles draw themselves
        self.worldLock.acquire()
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].draw(qp,i*incX,j*incY,
                                           incX+1,incY+1)
        self.worldLock.release()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()
        super().update()

    def getOptionsWidget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>World Options<\b>"))
        layout.addWidget(self.avgTempLabel)
        layout.addWidget(self.enableInvasiveBlack)
        layout.addWidget(QLabel("Invasive black optimal temp"))
        layout.addWidget(self.invasiveBlackTemp)
        layout.addWidget(self.enableInvasiveWhite)
        layout.addWidget(QLabel("Invasive white optimal temp"))
        layout.addWidget(self.invasiveWhiteTemp)
        layout.addWidget(self.resetButton)


        container = QWidget()
        container.setLayout(layout)
        return container

    def getTile(self,coords):
        return self.worldTiles[coords[0]%self.SIZE_X][coords[1]%self.SIZE_Y]
