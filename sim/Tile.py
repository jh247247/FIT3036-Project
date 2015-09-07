
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

from Daisy import Daisy

class Tile:
    BARE_ALBEDO = 0.5
    def __init__(self, parentWorld, temp):
        self.parent = parentWorld
        # TODO: Make different types of object that occupy this tile
        self.obj = None
        self.temp = temp

    def update(self, rad):
        if self.obj is not None:
            self.obj.update()
            # obj died, clear
            if self.obj.living is False:
                self.obj = None
        # else, the tile is unoccupied, attempt to spawn?
        else:
            self.spawn()


        # update temp
        if self.obj is not None:
            self.temp += 0.2*(rad*self.obj.albedo-0.5)
        else:
            self.temp += 0.2*(rad*self.BARE_ALBEDO-0.5)



    def spawn(self):
        chance = random.random()
        # TODO: make spawn chance dependent on the daisy type
        if chance < 1-abs(22.5-self.temp)/22.5-0.1: # TODO: fix magics
            # TODO: spawn different types of
            # daisy dependent on temperature
            if random.random() > (self.temp-22.5)/5+0.5:
                # TODO: make albedo not magic
                self.obj = Daisy(self, 0.7)
            else:
                self.obj = Daisy(self, 0.2)

    def draw(self, qp, x, y, w, h):
        # TODO: change this so it sets color, not albedo
        if self.obj is None:
            albedo = self.BARE_ALBEDO
        else:
            albedo = self.obj.albedo

        # convert albedo from "darkness" to lightness
        albedo = 255 - 255*albedo

        qp.setBrush(QColor(albedo,albedo,albedo))
        # draw in the albedo
        qp.drawRect(x,y,w,h)

        # overlay temp rect over the top
        qp.setBrush(QColor(min(max((self.temp-22.5)*50-255,0),255),
                         min(max(255-abs((self.temp-22.5)*50),0),255),
                           min(max(128-(self.temp-22.5)*50,0),255),25))


        qp.drawRect(x,y,w,h)


        qp.setPen(QColor(min(max((self.temp-22.5)*50-255,0),255),
                         min(max(255-abs((self.temp-22.5)*50),0),255),
                         min(max(128-(self.temp-22.5)*50,0),255)))

        # Write the temperature on the tile
        qp.drawText(QRectF(QPointF(x,y+h),
                           QPointF(x+w,y)),
                    Qt.AlignCenter,
                    str(round(self.temp,1)))

        qp.setPen(Qt.black);
