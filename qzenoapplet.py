import sys
import numpy as np
from PyQt5.QtWidgets import QSlider, QLineEdit, QDoubleSpinBox, QMenu, QRadioButton, QLabel, QSizePolicy, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QCursor, QPixmap
import csv
import datetime
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QDir
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from qiskit import *
# from functionpool import savedPara
from qiskit.visualization import plot_histogram

now = datetime.datetime.now()


class MainGui(QMainWindow):
    """This is the main window."""

    def __init__(self):
        super(MainGui, self).__init__()
        self.font = QFont('Sans Serif', 12)
        app.setFont(self.font)
        self.title = 'Quantum Zeno Effect'
        # self.left = 200
        # self.top = 50
        # self.width = 1400
        # self.height = 625
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        applet = Applet()
        self.setCentralWidget(applet)

        self.show()


class Applet(QWidget):
    def __init__(self):
        super(Applet, self).__init__()
        self.initapplet()




    def initapplet(self):

        self.grid = QVBoxLayout()
        self.calcs = QZenoEffectCalcs()
        self.sliders = self.sliderN()
        self.pics = self.figures(self.N)
        self.exp = self.experiment()
        # self.type = self.exptype()
        self.plot = WidgetPlot() #initialising the widget plot class

        self.grid.addWidget(self.sliders)
        self.grid.addWidget(self.exp)
        # self.grid.addWidget(self.type)
        self.box = QGroupBox()
        self.box.setLayout(self.grid)
        self.box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.pics)
        self.layout.addWidget(self.plot)

        self.setLayout(self.layout)

    def sliderN(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10000)
        self.N = self.slider.value()

        numbox = QDoubleSpinBox()
        numbox.setDecimals(0)
        numbox.setRange(self.slider.minimum(), self.slider.maximum())

        self.slider.valueChanged.connect(numbox.setValue)
        self.slider.rangeChanged.connect(numbox.setRange)
        numbox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.On_N_change)

        layout = QGridLayout()
        layout.addWidget(QLabel('Number of Beamsplitters'), 0, 0)
        layout.addWidget(numbox,1 , 0)
        layout.addWidget(self.slider, 1, 1)

        groupbox = QGroupBox()
        groupbox.setLayout(layout)
        groupbox.setTitle("Experiment Parameters")

        reflectlbl = QLabel('Reflectivity of Beamsplitters')

        self.reflectval = QLabel(str(round(np.pi/self.N, 4)))

        layout.addWidget(reflectlbl, 2, 0)
        layout.addWidget(self.reflectval, 2, 1)
        return groupbox

    def figures(self, N):

        groupbox = QGroupBox()
        groupbox.setStyleSheet('background-color: white;')
        groupbox.setFixedWidth(600)
        layout = QVBoxLayout()

        horizlayout1 = QHBoxLayout()
        horizlayout1.setContentsMargins(0,0,0,0)
        horizlayout1.setSpacing(0)
        groupbox.setLayout(layout)
        layout.addLayout(horizlayout1)


        fname = 'mirror.png'
        pix = QPixmap(fname)
        if N < 6:
            for i in range(N):
                beamsplitter_i = QLabel()
                beamsplitter_i.setPixmap(pix)
                horizlayout1.addWidget(beamsplitter_i)

        else:
            for i in range(6):
                beamsplitter_i = QLabel()
                beamsplitter_i.setPixmap(pix)
                horizlayout1.addWidget(beamsplitter_i)

        det = QLabel()
        # detpic = QPixmap('detector.png')
        det.setPixmap(QPixmap('detector.png'))
        horizlayout1.addWidget(det)

        horizlayout2 = QHBoxLayout()
        horizlayout2.setSpacing(0)
        horizlayout2.setContentsMargins(0,0,0,0)
        layout.addLayout(horizlayout2)
        if N < 6:
            circuit = self.calcs.zenocirc(N, 1)

            circuit.draw(filename='circuit.png', output='mpl')
            cir = QLabel()
            cirpic = QPixmap('circuit.png')
            cirpic.scaledToWidth(500)
            cirpic.scaledToHeight(500)

            cir.setPixmap(cirpic)


            horizlayout2.addWidget(cir)
        else:
            circuit = self.calcs.zenocirc(6, 1)

            circuit.draw(filename='circuit.png', output='mpl')
            cir = QLabel()
            cirpic = QPixmap('circuit.png')
            cirpic.scaledToWidth(500)
            cirpic.scaledToHeight(500)

            cir.setPixmap(cirpic)


            horizlayout2.addWidget(cir)
        return groupbox

    def experiment(self):
        nphotonslbl = QLabel('Number of Photons Sent through System:')
        self.nphotons = QLineEdit()
        self.nphotons.setText('1000')

        layout = QGridLayout()
        box = QGroupBox()
        box.setLayout(layout)
        # box.setTitle('')

        layout.addWidget(nphotonslbl, 0, 0)
        layout.addWidget(self.nphotons,1,0)

        exptypelayout = QHBoxLayout()
        self.typebeam = QRadioButton('Beamsplitters')
        self.typebeam.setChecked(True)
        self.typebeam.toggled.connect(lambda : self.exptypechange(self.typebeam))
        exptypelayout.addWidget(self.typebeam)

        self.typepolar = QRadioButton('Polarizers')
        typebox = QGroupBox()
        self.typepolar.toggled.connect(lambda : self.exptypechange(self.typepolar))
        exptypelayout.addWidget(self.typepolar)
        typebox.setLayout(exptypelayout)
        typebox.setTitle('Experiment Type')
        layout.addWidget(typebox,3,0,2,1)

        objecttypelayout = QHBoxLayout()
        self.yesobject = QRadioButton('Present')
        self.yesobject.setChecked(True)
        self.yesobject.toggled.connect(lambda: self.objtypechange(self.yesobject))
        objecttypelayout.addWidget(self.yesobject)

        self.noobject = QRadioButton('Not Present')
        self.noobject.toggled.connect(lambda: self.objtypechange(self.noobject))
        objecttypelayout.addWidget(self.noobject)
        objbox = QGroupBox()
        objbox.setLayout(objecttypelayout)
        objbox.setTitle('Is an Object Present')

        layout.addWidget(objbox, 6, 0, 2, 1)

        return box

    def results(self):
        box = QGroupBox()
        layout = QGridLayout()



    # def objectexist(self):
    #


    @pyqtSlot()
    def On_N_change(self):
        self.N = self.slider.value()
        self.layout.removeWidget(self.pics)
        self.pics = self.figures(self.N)
        self.layout.addWidget(self.pics)
        self.reflectivity = str(round(np.pi/self.N, 4))
        self.reflectval.setText(self.reflectivity)

    def exptypechange(self, type):
        if type.text() == 'Beamsplitters':
            if type.isChecked() ==True:
                self.exptype = 1
        if type.text() == 'Polarizers':
            if type.isChecked() ==True:
                self.exptype = 0

    def objtypechange(self, type):
        if type.text() == 'Present':
            if type.isChecked() ==True:
                self.objtype = 1
        if type.text() == 'Not Present':
            if type.isChecked() ==True:
                self.objtype = 0
    def on_thread_done(self, data):
        self.data = data #sets data to a global variable so we can call it in other functions
        self.plot.plot(data) #uses the QWidget class for plotting
        # result = execute(circuit, backend=self.backend, shots=1024).result()
        # counts = result.get_counts()
        # from qiskit.tools.visualization import plot_histogram
        # plot_histogram(counts)


class QZenoEffectCalcs():
    def theta(self, N):
        theta = np.pi/N
        return theta

    def transmitpredict(self, obj, N):
        theta = self.theta(N)
        if obj == 1:
            predict = (np.cos(theta/2)**2)**N
        if obj == 0:
            predict = 1-(np.sin(theta/2)**2)**N
        return predict

    def zenocirc(self, N, obj):
        theta = self.theta(N)

        q = QuantumRegister(1)
        c = ClassicalRegister(N)
        circuit = QuantumCircuit(q,c)
        for i in range(N):
            circuit.rx(theta, q[0])
            circuit.measure(q[0], c[i])

        return circuit

    def measure(self, nphotons, N, obj):
        circuit = self.zenocirc(N)
        endstate = '0' * N

        result = execute(circuit, backend=self.backend, shots=nphotons).result()
        counts = result.get_counts()
        ntrans = counts.get(endstate)
        pct = ntrans/nphotons
        predict = self.transmitpredict(obj, N)
        fname = 'circuit.png_'+N
        circuit.draw(filename=fname, output='mpl')

        return result, counts, ntrans, pct, predict


class PlotCanvas(FigureCanvas): #this creates a matplotlib canvas and defines some plotting aspects

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        plot_histogram(data)
        self.axes.set_title('Histogram of Measured States')
        self.draw()


class WidgetPlot(QWidget): #this converts the matplotlib canvas into a qt5 widget so we can implement it in the qt
    # framework laid out above
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.layout().addWidget(self.canvas)
        self.setFixedWidth(600)


    def plot(self, data):
        self.canvas.axes.clear() #it is important to clear out the plot first or everything just gets plotted on top of
        # each other and it becomes useless
        self.canvas.plot(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainGui()
    sys.exit(app.exec_())
