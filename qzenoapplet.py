import sys
import numpy as np
from PyQt5.QtWidgets import QSlider, QDoubleSpinBox, QMenu, QLabel, QSizePolicy, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QCursor
import csv
import datetime
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QDir
from qiskit import *
# from functionpool import savedPara
now = datetime.datetime.now()


class MainGui(QMainWindow):
    """This is the main window."""

    def __init__(self):
        super(MainGui, self).__init__()
        self.font = QFont('Sans Serif', 12)
        app.setFont(self.font)
        self.title = 'Quantum Zeno Effect'
        self.left = 200
        self.top = 50
        self.width = 1400
        self.height = 625
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        applet = Applet()
        self.setCentralWidget(applet)

        self.show()


class Applet(QWidget):
    def __init__(self):
        super(Applet, self).__init__()
        self.columns = 10
        self.initapplet()

    def initapplet(self):
        grid = QGridLayout()


        sliders = self.sliderbars()

        grid.addWidget(sliders)
        box = QGroupBox()
        box.setLayout(grid)
        box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        box.setTitle('Instrument Parameters')
        layout = QHBoxLayout()
        layout.addWidget(box)
        self.setLayout(layout)

    def sliderbars(self):
        groupbox = QGroupBox()
        layout = QGridLayout()
        groupbox.setLayout(layout)

        self.sliders = CustomSliders()
        numsplitterlabel = QLabel('Number of Beamsplitters')


        layout.addWidget(self.sliders, 0 , 0)



        return groupbox


    @pyqtSlot()
    def on_click_def(self):
        return

class CustomSliders(QWidget):
    def __init__(self, *args, **kwargs):
        super(CustomSliders, self).__init__(*args, **kwargs)
        self.N = 1
        self.refl = 3.14/self.N

        layout1, self.slider1 = self.sliderN()
        self.slider1.setValue(self.N)

        layout2, self.slider2 = self.sliderref()
        self.slider2.setValue(314159/self.N)

        # self.slider1.valueChanged.connect(self.numbersplitterslink())

        vlayout = QVBoxLayout(self)
        vlayout.addLayout(layout1)
        vlayout.addLayout(layout2)

        self.slider2.valueChanged.connect(lambda x: self.slider1.setValue(np.pi/x))


    def sliderN(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(10000)

        numbox = QDoubleSpinBox()
        numbox.setDecimals(2)
        numbox.setRange(slider.minimum(), slider.maximum())

        slider.valueChanged.connect(numbox.setValue)
        slider.rangeChanged.connect(numbox.setRange)
        numbox.valueChanged.connect(slider.setValue)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Number of Mirrors'))
        layout.addWidget(numbox)
        layout.addWidget(slider)

        return layout, slider

    def sliderref(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMaximum(314159)

        numbox = QDoubleSpinBox()
        numbox.setDecimals(5)
        numbox.setRange(slider.minimum(), slider.maximum())


        slider.valueChanged.connect(lambda x: numbox.setValue(x/100000))
        # slider.rangeChanged.connect(lambda x: numbox.setRange)
        numbox.valueChanged.connect(lambda x: slider.setValue(x * 100000))

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Reflectivity of Mirrors'))
        layout.addWidget(numbox)
        layout.addWidget(slider)

        return layout, slider

    @pyqtSlot()

    def numbersplitterslink(self):
        N = self.slider1.value()
        self.slider2.setValue(np.pi/N)
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainGui()
    sys.exit(app.exec_())
