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
        self.objtype = 1
        self.exptype = 1


        self.vlay = QVBoxLayout()
        self.calcs = QZenoEffectCalcs()
        self.sliders = self.sliderN()
        self.pics = self.figures(self.N)
        self.resultsbox = self.results()
        self.exp = self.experiment()
        # self.type = self.exptype()
        self.plot = WidgetPlot() #initialising the widget plot class

        self.vlay.addWidget(self.sliders)
        self.vlay.addWidget(self.exp)
        # self.grid.addWidget(self.type)
        self.box = QGroupBox()
        self.box.setLayout(self.vlay)
        self.box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.layout = QGridLayout()

        self.resultslay = QVBoxLayout()
        self.resultslay.addWidget(self.resultsbox)
        self.resultslay.addWidget(self.plot)

        self.layout.addWidget(self.box, 0, 0,)
        self.layout.addWidget(self.pics, 0, 1)
        self.layout.addLayout(self.resultslay, 0, 2)

        self.setLayout(self.layout)

    def sliderN(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(2)
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
        groupbox.setFixedWidth(650)
        layout = QVBoxLayout()

        horizlayout1 = QHBoxLayout()
        horizlayout1.setContentsMargins(0,0,0,0)
        horizlayout1.setSpacing(0)
        groupbox.setLayout(layout)
        layout.addLayout(horizlayout1)



        if N < 6:
            if self.exptype == 1:
                if self.objtype ==1 :
                    fname = 'figures_zeno/'+str(N)+'beamsplitter_object_combined.png'
                    pix = QPixmap(fname)
                    pix = pix.scaled(600, 600, Qt.KeepAspectRatio)

                    beamsplitter_i = QLabel()
                    beamsplitter_i.setPixmap(pix)
                    horizlayout1.addWidget(beamsplitter_i)
                if self.objtype == 0 :
                    fname = 'figures_zeno/'+str(N)+'beamsplitter_noobject_combined.png'
                    pix = QPixmap(fname)
                    pix = pix.scaled(600, 600, Qt.KeepAspectRatio)

                    beamsplitter_i = QLabel()
                    beamsplitter_i.setPixmap(pix)
                    horizlayout1.addWidget(beamsplitter_i)

        else:
            if self.exptype == 1:
                if self.objtype ==1 :
                    fname = 'figures_zeno/Nbeamsplitter_object_combined.png'
                    pix = QPixmap(fname)
                    pix = pix.scaled(600, 600, Qt.KeepAspectRatio)

                    beamsplitter_i = QLabel()
                    beamsplitter_i.setPixmap(pix)
                    horizlayout1.addWidget(beamsplitter_i)
                if self.objtype == 0 :
                    fname = 'figures_zeno/Nbeamsplitter_noobject_combined.png'
                    pix = QPixmap(fname)
                    pix = pix.scaled(600, 600, Qt.KeepAspectRatio)

                    beamsplitter_i = QLabel()
                    beamsplitter_i.setPixmap(pix)
                    horizlayout1.addWidget(beamsplitter_i)

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

        self.runbtn = QPushButton('Run Simulation')
        layout.addWidget(self.runbtn, 8, 0)
        self.runbtn.clicked.connect(self.on_click_runsim)

        return box

    def results(self):
        box = QGroupBox()
        layout = QGridLayout()
        label = QLabel('Experiment Results')
        self.ntranslbl = QLabel('Number Transmited:')
        self.ntransnum = QLabel('')
        self.pcttranslbl = QLabel('Percent Transmitted:')
        self.pcttransnum = QLabel('')
        self.theorylbl = QLabel('Theoretical Prediction Percent:')
        self.theorynum = QLabel('')

        box.setLayout(layout)
        layout.addWidget(label, 0, 0,)
        layout.addWidget(self.ntranslbl, 1, 0)
        layout.addWidget(self.ntransnum, 1, 1)
        layout.addWidget(self.pcttranslbl, 2, 0)
        layout.addWidget(self.pcttransnum, 2, 1)
        layout.addWidget(self.theorylbl, 3, 0)
        layout.addWidget(self.theorynum, 3, 1)


        return box



    # def objectexist(self):
    #


    @pyqtSlot()
    def On_N_change(self):
        self.N = self.slider.value()
        self.layout.removeWidget(self.pics)
        self.pics = self.figures(self.N)
        self.layout.addWidget(self.pics, 0, 1)
        self.reflectivity = str(round(np.pi/self.N, 4))
        self.reflectval.setText(self.reflectivity)

    def exptypechange(self, type):
        if type.text() == 'Beamsplitters':
            if type.isChecked() ==True:
                self.exptype = 1
                print('Beamsplitters', self.exptype)
        if type.text() == 'Polarizers':
            if type.isChecked() ==True:
                print('Polarizers', self.exptype)
                self.exptype = 0

    def objtypechange(self, type):
        if type.text() == 'Present':
            if type.isChecked() ==True:
                self.objtype = 1
                self.layout.removeWidget(self.pics)
                self.pics = self.figures(self.N)
                self.layout.addWidget(self.pics, 0, 1)
                print('Present', self.objtype)

        if type.text() == 'Not Present':
            if type.isChecked() ==True:
                self.objtype = 0
                self.layout.removeWidget(self.pics)
                self.pics = self.figures(self.N)
                self.layout.addWidget(self.pics, 0, 1)
                print('Not present', self.objtype)

    def on_click_runsim(self):

        if self.objtype ==1:
            n = int(self.nphotons.text())
            result, counts, ntrans, pct, predict = self.calcs.measure(n, self.N, 1)


        if self.objtype ==0:
            n = int(self.nphotons.text())
            result, counts, ntrans, pct, predict = self.calcs.measure(n, self.N, 0)
            from qiskit.tools.visualization import plot_histogram
            self.plot.plot(counts)

        self.ntransnum.setText(str(ntrans))
        self.theorynum.setText(str(predict))
        self.pcttransnum.setText(str(pct))




class QZenoEffectCalcs():
    def theta(self, N):
        theta = np.pi/N
        # print('theta = ', theta)
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
        if obj == 1 :
            q = QuantumRegister(1)
            c = ClassicalRegister(N)
            circuit = QuantumCircuit(q,c)
            for i in range(N):
                circuit.rx(theta, q[0])
                circuit.measure(q[0], c[i])

        if obj == 0:
            q = QuantumRegister(1)
            c = ClassicalRegister(1)
            circuit = QuantumCircuit(q,c)
            for i in range(N):
                circuit.rx(theta, q[0])
                circuit.measure(q[0], c[0])
        # print(circuit)
        return circuit

    def measure(self, nphotons, N, obj):
        self.backend = Aer.get_backend('qasm_simulator')
        # print('backend set')
        circuit = self.zenocirc(N, obj)
        # print('circuit made')
        endstate = '0' * N
        # print('endstate set')

        result = execute(circuit, backend=self.backend, shots=nphotons).result()
        # print('simulation done')
        counts = result.get_counts()
        ntrans = counts.get(endstate)
        if counts.get(endstate) == None:
            ntrans = 0
        # print('photons=',nphotons)
        # print('transmitted=', ntrans)
        pct = ntrans/nphotons

        predict = self.transmitpredict(obj, N)
        # fname = 'circuit.png_'+N
        # circuit.draw(filename=fname, output='mpl')
        # print(result, counts, ntrans, pct, predict)

        return result, counts, ntrans, pct, predict



class PlotCanvas(FigureCanvas): #this creates a matplotlib canvas and defines some plotting aspects

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        plot_histogram(data, ax = self.axes)
        self.axes.set_title('Histogram of Measured States')


class WidgetPlot(QWidget): #this converts the matplotlib canvas into a qt5 widget so we can implement it in the qt
    # framework laid out above
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.layout().addWidget(self.canvas)
        self.setFixedWidth(400)


    def plot(self, data):
        self.canvas.axes.clear() #it is important to clear out the plot first or everything just gets plotted on top of
        # each other and it becomes useless
        self.canvas.plot(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainGui()
    sys.exit(app.exec_())
