
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

from Daisy import Daisy

class Tile:
    BARE_ALBEDO = 0.5
    def __init__(self, parentWorld, temp):
        self.parent = parentWorld
        # TODO: Make different types of object that occupy this tile
        self.obj = None
        self.temp = temp

    def update(self):
        # TODO: update temp based on incoming incident radiation
        if self.obj is not None:
            self.obj.update()
            # obj died, clear
            if self.obj.living is False:
                self.obj = None
        # else, the tile is unoccupied, attempt to spawn?
        else:
            print("Making daisy!")
            self.obj = Daisy(self, random.random())

    def draw(self, qp, x, y, w, h):
        if self.obj is None:
            albedo = self.BARE_ALBEDO
        else:
            albedo = self.obj.albedo

        # convert albedo from "darkness" to lightness
        albedo = 255 - 255*albedo

        qp.setBrush(QColor(albedo,albedo,albedo))
        # draw in the albedo
        qp.drawRect(x,y,w,h)
        qp.setPen(Qt.red)

        # FIXME: nasty magicses
        qp.drawText(x,y+h,str(self.temp))
        # TODO: Write the temperature on the tile
        qp.setPen(Qt.black)
