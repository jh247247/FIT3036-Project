import sys
import threading

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

from Tile import Tile
from Sun import Sun

class World(QWidget):
    SIZE_X = 20
    SIZE_Y = 20
    START_TEMP = 20
    def __init__(self, sun):
        super().__init__()

        self.sun = sun

        # calculate start temp from sun
        self.avgTemp = self.START_TEMP
        # TODO: variation dependent on the position of the tile?
        self.worldTiles = [[Tile(self, World.START_TEMP) \
                            for x in range(self.SIZE_X)] \
                           for y in range(self.SIZE_Y)]
        self.worldLock = threading.Lock()

        self.update()

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()


    def update(self):
        self.worldLock.acquire()

        threading.Timer(0.001,self.update).start()
        self.avgTemp = 0
        # let the tiles update their temps
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].update(self.sun.radiation)


        # TODO: let the temperature of adjacent tiles affect each other
        # Cannot do this in place, have to make an array of whatever
        # change is required and apply it, multiple times for multiple
        # stages?

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
                deltaTempTiles[i][j] *= 0.1

        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].temp -= deltaTempTiles[i][j]

        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.avgTemp += self.worldTiles[i][j].temp

        self.worldLock.release()
        self.avgTemp /= self.SIZE_X*self.SIZE_Y
        self.sun.update()
        print(str(self.avgTemp) + " , " + str(self.sun.radiation))


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = World(Sun())
    sys.exit(app.exec_())
