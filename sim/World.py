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
    START_TEMP = 22.5
    def __init__(self, sun):
        super().__init__()

        # calculate start temp from sun
        self.avgTemp = self.START_TEMP
        # TODO: variation dependent on the position of the tile?
        self.worldTiles = [[Tile(self, World.START_TEMP) \
                            for x in range(self.SIZE_X)] \
                           for y in range(self.SIZE_Y)]

        self.update()

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()


    def update(self):
        threading.Timer(0.1,self.update).start()
        # let the tiles draw themselves
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].update()


    def draw(self, qp):
        size = self.size()
        incX = size.width()/self.SIZE_X
        incY = size.height()/self.SIZE_Y

        # let the tiles draw themselves
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                self.worldTiles[i][j].draw(qp,i*incX,j*incY,
                                           incX+1,incY+1)


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()
        super().update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = World(None)
    sys.exit(app.exec_())
