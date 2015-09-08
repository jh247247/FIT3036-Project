from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# handles the interface to the user in the "sidebar"

class InterfaceHandler(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(300)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout);
        
    def addWidget(self, widget):
        # make a nice seperator between new widgets
        if(self.layout.count() != 0):
            sep = QFrame()
            sep.setFrameShape(QFrame.HLine)
            sep.setFrameShadow(QFrame.Sunken)
            self.layout.addWidget(sep)

        self.layout.addWidget(widget)
