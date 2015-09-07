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
        self.radSpinner.valueChanged.connect(self.handleRadSpinner)

        self.deltaSpinner = QDoubleSpinBox(self)
        self.deltaSpinner.valueChanged.connect(self.handleDeltaSpinner)

        self.deltaEnable = QCheckBox(self)
        self.deltaEnable.setText("Enable radiation delta")

        # text that we don't need to keep a reference to
        title = QLabel("<b>Sun Options<\b>",self)
        radText = QLabel("Current Radiation:",self)
        deltaText = QLabel("Change per tick",self)

        # add widgets to layout
        self.mainLayout.addWidget(title)
        self.mainLayout.addWidget(radText)
        self.mainLayout.addWidget(self.radSpinner)
        self.mainLayout.addWidget(deltaText)
        self.mainLayout.addWidget(self.deltaSpinner)
        self.mainLayout.addWidget(self.deltaEnable)

    def handleRadSpinner(self, val):
        self.radiation = val

    def handleDeltaSpinner(self,val):
        self.delta = val

    def update(self):
        self.radiation += self.delta
