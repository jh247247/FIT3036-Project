#!/usr/bin/python3
import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Sun import Sun
from World import World
from InterfaceHandler import InterfaceHandler

class DaisyWorld(QWidget):

    def __init__(self):
        super().__init__()

        # make World stuff
        self.sun = Sun()
        self.world = World(self.sun)


        self.initUI()


    def initUI(self):
        # interface handler
        self.interfaceHandler = InterfaceHandler()
        self.interfaceHandler.addWidget(self.sun);
        self.interfaceHandler.addWidget(self.world.getOptionsWidget());


        # Make layout
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.interfaceHandler)
        self.mainLayout.addWidget(self.world)



        # set dims for window
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('DaisyWorld')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DaisyWorld()
    sys.exit(app.exec_())
