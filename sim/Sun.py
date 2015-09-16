from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Sun(QWidget):
    def __init__(self,args):
        super().__init__()
        # radiation value of 1 means that if albedo is 0.5,
        # temperature should eventually become 22.5
        self.radiation = args.radiation[0]
        self.delta = args.delta[0]
        self.initUI()

        if self.delta is not 0:
            self.deltaEnable.setChecked(True)

    def initUI(self):
        # make it so the widget doesnt take up the entire screen
        self.setMaximumWidth(300)
        self.mainLayout = QVBoxLayout(self);

        self.radSpinner = QDoubleSpinBox(self)
        self.radSpinner.setDecimals(4)
        self.radSpinner.setValue(1) # set the default radiation value
        self.radSpinner.setSingleStep(0.0001)
        self.radSpinner.valueChanged.connect(self.handleRadSpinner)

        self.deltaSpinner = QDoubleSpinBox(self)
        self.deltaSpinner.setDecimals(4)
        self.deltaSpinner.setSingleStep(0.0001)
        self.deltaSpinner.setMinimum(-1)
        self.deltaSpinner.setMaximum(1)
        self.deltaSpinner.valueChanged.connect(self.handleDeltaSpinner)

        self.deltaEnable = QCheckBox(self)
        self.deltaEnable.setText("Enable radiation delta")

        # text that we don't need to keep a reference to
        title = QLabel("<b>Sun Options<\b>",self)
        self.radText = QLabel("Current Radiation: " + str(round(self.radiation,4)),self)
        seedRadText = QLabel("Seed radiation:",self)
        deltaText = QLabel("Change per tick",self)

        # add widgets to layout
        self.mainLayout.addWidget(title)
        self.mainLayout.addWidget(self.radText)
        self.mainLayout.addWidget(seedRadText)
        self.mainLayout.addWidget(self.radSpinner)
        self.mainLayout.addWidget(deltaText)
        self.mainLayout.addWidget(self.deltaSpinner)
        self.mainLayout.addWidget(self.deltaEnable)

    def handleRadSpinner(self, val):
        self.radiation = val

    def handleDeltaSpinner(self,val):
        self.delta = val

    def update(self):
        if self.deltaEnable.isChecked():
            self.radiation += self.delta
        self.radText.setText("Current Radiation: " + str(round(self.radiation,4)))
