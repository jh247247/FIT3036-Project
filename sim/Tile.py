
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

from Daisy import Daisy
import DaisyFactory

class Tile:
    BARE_ALBEDO = 0.5
    def __init__(self, parentWorld, temp, coords):
        self.parent = parentWorld
        self.obj = None
        self.temp = temp
        self.coords = coords

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
        # TODO: fix fudge factor.
        if self.obj is not None:
            self.temp += 0.1*(rad*self.obj.albedo-0.5)
        else:
            self.temp += 0.1*(rad*self.BARE_ALBEDO-0.5)



    def spawn(self):
        self.obj = DaisyFactory.createDaisy(self)

    def draw(self, qp, x, y, w, h):
        # TODO: change this so it sets color, not albedo
        if self.obj is None:
            qp.setBrush(QColor(0,128,0))
        else:
            # convert albedo from "darkness" to lightness
            color = 255-255*self.obj.albedo
            qp.setBrush(QColor(min(max(color+(self.obj.optTemp-22.5)*5,0),255),
                               color,
                               min(max(color+(22.5-self.obj.optTemp)*5,0),255)))

        # draw in the albedo
        qp.drawRect(x,y,w,h)

        # overlay temp rect over the top
                        # qp.setBrush(QColor(min(max((self.temp-22.5)*50-255,0),255),
                        #                  min(max(255-abs((self.temp-22.5)*50),0),255),
                        #                    min(max(128-(self.temp-22.5)*50,0),255),25))


        # qp.drawRect(x,y,w,h)


        qp.setPen(QColor(min(max((self.temp-22.5)*128-255,0),255),
                         0,
                         min(max(-(self.temp-22.5)*50,0),255)))

        # Write the temperature on the tile
        qp.drawText(QRectF(QPointF(x,y+h),
                           QPointF(x+w,y)),
                    Qt.AlignCenter,
                    str(round(self.temp,1)))

        qp.setPen(Qt.black);
