from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class World(QWidget):
    SIZE_X = 10
    SIZE_Y = 10
    def __init__(self, sun):
        super().__init__()
        # calculate start temp from sun
        self.startTemp = 22.5
        # TODO: variation dependent on the position of the tile?
        self.tileTemp = [[self.startTemp for x in range(SIZE_X)]
                         for y in range(SIZE_Y)]
        self.worldTiles = [[Tile() for x in range(SIZE_X)]
                           for y in range(SIZE_Y)]

    def update(self):
        i = 0
        # TODO: update temps at each tile area
        # TODO: update objects at each tile

    def draw(self):
        i = 0
        # TODO: draw each object to a given canvas
        # TODO: figure out how to pass in the dims

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin.self()
        # TODO: actual drawing of tiles
        qp.end()
