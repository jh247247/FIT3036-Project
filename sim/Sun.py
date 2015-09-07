from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Sun(QWidget):
    def __init__(self):
        super().__init__()
        # radiation value of 1 means that if albedo is 0.5,
        # temperature should eventually become 22.5
        self.radiation = 1.0
        self.delta = 0
        self.initUI()

    def initUI(self):
        # make it so the widget doesnt take up the entire screen
        self.setMaximumWidth(300)
        self.mainLayout = QVBoxLayout(self);
        self.radSpinner = QDoubleSpinBox(self)
        self.deltaSpinner = QDoubleSpinBox(self)
        title = QLabel("<b>Sun Options<\b>",self)
        radText = QLabel("Current Radiation:",self)
        deltaText = QLabel("Change per tick",self)


        self.mainLayout.addWidget(title)
        self.mainLayout.addWidget(radText)
        self.mainLayout.addWidget(self.radSpinner)
        self.mainLayout.addWidget(deltaText)
        self.mainLayout.addWidget(self.deltaSpinner)

    def update(self):
        self.radiation += self.delta
        # TODO: make radiation an actual equation that takes in time
