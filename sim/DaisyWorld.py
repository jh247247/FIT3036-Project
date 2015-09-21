#!/usr/bin/python3
import sys, random
import argparse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Sun import Sun
from World import World
from InterfaceHandler import InterfaceHandler

class DaisyWorld(QWidget):

    def __init__(self, args):
        super().__init__()

        # make World stuff
        self.sun = Sun(args)
        self.world = World(self.sun,args)

        if args.no_gui is False:
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
    parser = argparse.ArgumentParser(description="Simulation for daisyworld")
    parser.add_argument('-g', '--no-gui', action='store_true',
                        help='Do not display UI')
    parser.add_argument('-t', '--temp',metavar='T', type=float, nargs=1,
                        default=World.START_TEMP,
                        help='Set universal starting temp to T')
    parser.add_argument('-s', '--stop-tick',metavar='S', type=float, nargs='?',
                        default=0,
                        help='Stop simulation at time tick S')
    parser.add_argument('-b', '--iblack' ,metavar='B', type=float, nargs='?',
                        default=0,
                        help='Enable invasive black daisies with temp B')
    parser.add_argument('-w', '--iwhite',metavar='W', type=float, nargs='?',
                        default=0,
                        help='Enable invasive white daisies with temp W')
    parser.add_argument('-r', '--radiation',metavar='R', type=float, nargs=1,
                        default=[1.0],
                        help='Set initial sun radiation R')
    parser.add_argument('-d', '--delta',metavar='D', type=float, nargs=1,
                        default=[0.0],
                        help='Set radiation change per tick D')



    args = parser.parse_args()

    random.seed()

    app = QApplication(sys.argv)

    ex = DaisyWorld(args)

    if args.no_gui is False:
        sys.exit(app.exec_())
