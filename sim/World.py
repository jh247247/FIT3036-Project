import sys, random
import threading
import itertools

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Tile import Tile
from Sun import Sun
import DaisyFactory


class World(QWidget):
    SIZE_X = 50
    SIZE_Y = 50
    START_TEMP = 22.5
    BOLTZMANN_CONSTANT = 5.670373e-8
    SUN_WATTMETER_PER_UNIT = 3458.62
    def __init__(self, sun, args):
        super().__init__()

        self.sun = sun
        self.tick = 0
        self.stop_tick = args.stop_tick
        if args.no_gui is True:
            self.tick_time = 0
        else:
            self.tick_time = 0.001

        # calculate start temp from sun
        self.avgTemp = args.temp[0]
        self.avgAlbedo = 0

        # init temp from given val
        self.worldLock = threading.Lock()
        self.resetWorld()


        self.initOptionsUI()
        DaisyFactory.setWorld(self)


        if args.iblack is not 0:
            self.enableInvasiveBlack.setChecked(True)
            self.invasiveBlackTemp.setValue(args.iblack)

        if args.iwhite is not 0:
            self.enableInvasiveWhite.setChecked(True)
            self.invasiveWhiteTemp.setValue(args.iwhite)

        DaisyFactory.updateAttr()

        self.threadRunning = True

        threading.Thread(target=self.updateLoop).start()


    def closeEvent(self, event):
        self.threadRunning = False

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
        self.linWorld = list(itertools.chain(*self.worldTiles))
        self.worldLock.release()

        self.tick = 0


    def updateOptionsUI(self):
        self.avgTempLabel.setText("Average temp: " +
                                  str(round(self.avgTemp,4)))

    def updateLoop(self):
        while True:
            self.update()

    def update(self):
        self.worldLock.acquire()

        # calculate average temperature and albedo of world
        self.avgTemp = 0
        self.avgAlbedo = 0
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.avgTemp += self.worldTiles[i][j].temp
                self.avgAlbedo += self.worldTiles[i][j].albedo
        self.avgTemp /= self.SIZE_X*self.SIZE_Y
        self.avgAlbedo /= self.SIZE_X*self.SIZE_Y

        # calculate emission temp of world (i.e: temp of world if
        # daisies do not die and left to stabilize at current radiation)
        self.expectedTemp = (self.sun.radiation*self.SUN_WATTMETER_PER_UNIT/ \
                        (4*self.BOLTZMANN_CONSTANT)* \
                        (self.avgAlbedo)) \
                        **(1/4)

        self.emissionTemp = (self.sun.radiation*self.SUN_WATTMETER_PER_UNIT/ \
                        (4*self.BOLTZMANN_CONSTANT)* \
                        (0.5)) \
                        **(1/4)


        print(str(self.avgTemp) + " , " + \
              str(self.sun.radiation) + \
              " , "+ str(self.tick) \
              + " , " + str(1-self.avgAlbedo) \
              + " , " + str(self.emissionTemp-273)
              + " , " + str(self.expectedTemp-273))

        self.tick += 1
        if self.stop_tick is not 0 and self.tick > self.stop_tick:
            self.threadRunning = False
            quit() # could be more elegant..

        random.shuffle(self.linWorld)
        for t in self.linWorld:
            t.update(self.sun.radiation,self.emissionTemp-273)


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

        self.worldLock.release()

        self.sun.update()


    def draw(self, qp):
        size = self.size()
        incX = size.width()/self.SIZE_X
        incY = size.height()/self.SIZE_Y


        # let the tiles draw themselves
        self.worldLock.acquire()
        self.updateOptionsUI()
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
