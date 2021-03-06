# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qiskit import *
from qiskit.tools.visualization import plot_bloch_multivector
import numpy as np
import matplotlib as matplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

counter = 0

qr = QuantumRegister(3)
cr = ClassicalRegister(3)
qc = QuantumCircuit(qr, cr)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1900, 978)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 790, 88, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.circuitDiagram = QtWidgets.QLabel(self.centralwidget)
        self.circuitDiagram.setGeometry(QtCore.QRect(1270, 340, 561, 281))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.circuitDiagram.setFont(font)
        self.circuitDiagram.setText("")
        self.circuitDiagram.setScaledContents(True)
        self.circuitDiagram.setObjectName("circuitDiagram")
        self.pushResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushResetButton.setGeometry(QtCore.QRect(70, 870, 88, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushResetButton.setFont(font)
        self.pushResetButton.setObjectName("pushResetButton")
        self.stepCountLabel = QtWidgets.QLabel(self.centralwidget)
        self.stepCountLabel.setGeometry(QtCore.QRect(270, 790, 31, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepCountLabel.setFont(font)
        self.stepCountLabel.setObjectName("stepCountLabel")
        self.stepCounterDynamic = QtWidgets.QLabel(self.centralwidget)
        self.stepCounterDynamic.setGeometry(QtCore.QRect(330, 790, 41, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepCounterDynamic.setFont(font)
        self.stepCounterDynamic.setObjectName("stepCounterDynamic")
        self.blochSphere = QtWidgets.QLabel(self.centralwidget)
        self.blochSphere.setGeometry(QtCore.QRect(480, 370, 671, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.blochSphere.setFont(font)
        self.blochSphere.setText("")
        self.blochSphere.setScaledContents(True)
        self.blochSphere.setObjectName("blochSphere")
        self.atomTransition = QtWidgets.QLabel(self.centralwidget)
        self.atomTransition.setGeometry(QtCore.QRect(80, 240, 311, 491))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.atomTransition.setFont(font)
        self.atomTransition.setText("")
        self.atomTransition.setScaledContents(True)
        self.atomTransition.setObjectName("atomTransition")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(270, 820, 121, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.stepDescription = QtWidgets.QLabel(self.centralwidget)
        self.stepDescription.setGeometry(QtCore.QRect(400, 770, 661, 161))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepDescription.setFont(font)
        self.stepDescription.setText("")
        self.stepDescription.setObjectName("stepDescription")
        self.histogram = QtWidgets.QLabel(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(1420, 690, 361, 261))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.histogram.setFont(font)
        self.histogram.setObjectName("histogram")
        self.histogram.setScaledContents(True)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 180, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(480, 180, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1250, 180, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setGeometry(QtCore.QRect(1140, 790, 211, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.SelectTrials = QtWidgets.QComboBox(self.centralwidget)
        self.SelectTrials.setGeometry(QtCore.QRect(1270, 840, 101, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SelectTrials.setFont(font)
        self.SelectTrials.setObjectName("SelectTrials")
        self.SelectTrials.addItem("")
        self.SelectTrials.addItem("")
        self.SelectTrials.addItem("")
        self.SelectTrials.addItem("")
        self.SelectTrials.addItem("")
        self.stepCountLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.stepCountLabel_2.setGeometry(QtCore.QRect(1140, 840, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepCountLabel_2.setFont(font)
        self.stepCountLabel_2.setObjectName("stepCountLabel_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 220, 521, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.stepDescription_2 = QtWidgets.QLabel(self.centralwidget)
        self.stepDescription_2.setGeometry(QtCore.QRect(350, 80, 1121, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.stepDescription_2.setFont(font)
        self.stepDescription_2.setObjectName("stepDescription_2")
        self.stepDescription_3 = QtWidgets.QLabel(self.centralwidget)
        self.stepDescription_3.setGeometry(QtCore.QRect(720, 20, 401, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.stepDescription_3.setFont(font)
        self.stepDescription_3.setObjectName("stepDescription_3")
        self.stepDescription_4 = QtWidgets.QLabel(self.centralwidget)
        self.stepDescription_4.setGeometry(QtCore.QRect(1620, 50, 161, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepDescription_4.setFont(font)
        self.stepDescription_4.setObjectName("stepDescription_4")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setGeometry(QtCore.QRect(70, 830, 88, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButtonBack.setFont(font)
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.stepDescription_5 = QtWidgets.QLabel(self.centralwidget)
        self.stepDescription_5.setGeometry(QtCore.QRect(1620, 0, 171, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(22)
        font.setItalic(True)
        self.stepDescription_5.setFont(font)
        self.stepDescription_5.setObjectName("stepDescription_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Hiding histogram button and label 
        self.hideHistogramBatch()

        #event listeners configuration
        #code to invoke quantum modules for calculations
        self.pushButton.clicked.connect(self.updateCounterForNextButton)

        #previous step
        self.pushButtonBack.clicked.connect(self.updateCounterForPreviousButton)

        # Reset button 
        self.pushResetButton.clicked.connect(self.resetDashBoard)
        #Histogram click event
        self.pushButton_3.clicked.connect(self.showHistogramData)

        #initial states of qubits on Bloch sphere
        self.blochSphere.setPixmap(QtGui.QPixmap('./img0_BlochDiagram'))

        #initial states of electrons in the atom
        self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img0_AtomConfig'))

        self.stepDescription.setText("The qubit states denoted as |up> and |down> are encoded in the NV\n"
            "spin sub-levels m_s = 0 and m_s = -1 respectively. m_s is the spin\n"
            "quantum number which describes angular momentum of an electron.\n"
            "The spins are initialized to |up> state")
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Next"))
        self.pushResetButton.setText(_translate("MainWindow", "Reset"))
        self.stepCountLabel.setText(_translate("MainWindow", "Step"))
        self.stepCounterDynamic.setText(_translate("MainWindow", "0"))
        self.label_6.setText(_translate("MainWindow", "Step Description"))
        self.histogram.setText(_translate("MainWindow", "Histogram"))
        self.label.setText(_translate("MainWindow", "Atomic picture"))
        self.label_2.setText(_translate("MainWindow", "Bloch diagram"))
        self.label_3.setText(_translate("MainWindow", "Circuit Diagram"))
        self.pushButton_3.setText(_translate("MainWindow", "Click here for Histogram"))
        self.SelectTrials.setItemText(0, _translate("MainWindow", "1"))
        self.SelectTrials.setItemText(1, _translate("MainWindow", "10"))
        self.SelectTrials.setItemText(2, _translate("MainWindow", "1000"))
        self.SelectTrials.setItemText(3, _translate("MainWindow", "10000"))
        self.SelectTrials.setItemText(4, _translate("MainWindow", "1000000"))
        self.stepCountLabel_2.setText(_translate("MainWindow", "Number of trials:"))
        self.label_4.setText(_translate("MainWindow", "Qubit 0 - solid state spin, qubit 1 - Early photon, qubit 2 - Late Photon"))
        self.stepDescription_2.setText(_translate("MainWindow", "This demo is designed to help understand the process of quantum entanglement between the time bin of the photon emission and\n"
"the electronic spin of a nitrogen vacancy (NV) in diamond"))
        self.stepDescription_3.setText(_translate("MainWindow", "Spin-photon entanglement"))
        self.stepDescription_4.setText(_translate("MainWindow", "Demo by:\n"
            "Sridhar Majety\n"
            "Victoria A. Norman\n"
            "Liang Li\n"
            "Jesse Patton"))
        self.pushButtonBack.setText(_translate("MainWindow", "Previous"))
        self.stepDescription_5.setText(_translate("MainWindow", "quid pro quo"))


    def updateCounterForNextButton(self,MainWindow):
        global counter 
        if counter<4:
            counter = counter + 1
            self.updateCircuitDiagram(MainWindow)

    def updateCounterForPreviousButton(self,MainWindow):
        global counter
        if counter>0:
            counter = counter - 1
            self.updateCircuitDiagram(MainWindow)

    # code to get circuit data from quiskit
    def updateCircuitDiagram(self,MainWindow):
        global counter 
        self.updateCounterStepLabel()
        print("updateCircuitDiagram ")
        print(str(counter))
        #Hiding histograms when counter not 4
        if counter != 4 :
             self.hideHistogramBatch()
        if counter ==0:
            self.resetDashBoard()        
        if counter == 1:
            self.circuitDiagram.setPixmap(QtGui.QPixmap('./img1_CircuitDiagram'))
            self.blochSphere.setPixmap(QtGui.QPixmap('./img1_BlochDiagram'))
            ##edited this
            #self.blochSphere.setPixmap(QtGui.QPixmap('./img1_BlochDiagram').scaled(64,64,Qt.KeepAspectRatio))
            self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img1_AtomConfig'))
            self.updateStepDescription("Applying a pi/2 pulse will create an equal superposition of |up> and\n"
            "|down> spins.\n"
            "It should be noted in the Bloch diagram that the arrow denoting qubit 0\n"
            "rotated by pi/2 about the y-axis corresponding to pi/2 rotation gate about\n"
            "y-axis in the circuit diagram.")
        if counter == 2:
            self.circuitDiagram.setPixmap(QtGui.QPixmap('./img2_CircuitDiagram'))
            self.blochSphere.setPixmap(QtGui.QPixmap('./img2_BlochDiagram'))
            self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img2_AtomConfig'))
            self.updateStepDescription("A laser pulse selectively excites the |up> spin to the excited state |e>\n"
                "and |down> spin remains in the same level unaffected.\n" 
                "A spontaneous emission of photon is followed which locally entangles the\n"
                "qubit and photon number. In the state notation, 1 denotes presence of an\n"
                "emitted 'EARLY' photon and 0 denotes absence of an emitted 'EARLY' photon.\n"
                "Note that there are no arrows in the Bloch sphere of qubit 0 and 1 since\n"
                "they are entangled and the qubits need to be measured to know their values.")
        if counter == 3:
            self.circuitDiagram.setPixmap(QtGui.QPixmap('./img3_CircuitDiagram'))
            self.blochSphere.setPixmap(QtGui.QPixmap('./img3_BlochDiagram'))
            self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img3_AtomConfig'))
            self.updateStepDescription("The superposition of the spin is now inverted by applying a pi pulse.\n"
                "Note that the |up> and |down> positions are interchanged in the state\n"
                "notation.")
        if counter == 4:
            self.circuitDiagram.setPixmap(QtGui.QPixmap('./img4_CircuitDiagram'))
            self.blochSphere.setPixmap(QtGui.QPixmap('./img4_BlochDiagram'))
            self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img4_AtomConfig'))
            self.updateStepDescription("A second laser pulse is used to excite the |up> spin to |e> and a\n"
                "spontaneous emission results in a 'LATE' photon. From the state notation it\n"
                "should be noted that for the combination of qubit 1 and 2, 10 and 01 are\n"
                "the only possibilities which can be labelled as 'EARLY' and 'LATE' photons\n"
                "respectively. This is the protocol we use to achieve entanglement between\n"
                "the spin state and the time bin in which photon is emitted.\n"
                "SELECT NUMBER OF TRIALS TO SEE STATISTICS OF THE POSSIBLE OUTCOMES ----->")
            self.pushButton_3.setHidden(False)
            self.SelectTrials.setHidden(False)
            self.stepCountLabel_2.setHidden(False)


    



        

    def inititalizeQbitStates(self):
        global qr 
        global cr 
        global qc
        backend = Aer.get_backend('statevector_simulator')
        out = execute(qc,backend).result().get_statevector()
        fig0 = plot_bloch_multivector(out)
        fig0.savefig("./img0_BlochDiagram")

        # step-1 for counter =1 
        qc.ry(np.pi/2, 0) #pi/2 rotation of q0
        qc.draw(output='mpl',filename='./img1_CircuitDiagram')
        backend = Aer.get_backend('statevector_simulator')
        out = execute(qc,backend).result().get_statevector()
        fig1 = plot_bloch_multivector(out)
        fig1.savefig("./img1_BlochDiagram")

        # step-2 for counter =2
        qc.cx(0, 1)
        qc.draw(output='mpl',filename='./img2_CircuitDiagram')
        backend = Aer.get_backend('statevector_simulator')
        out = execute(qc,backend).result().get_statevector()
        fig2 = plot_bloch_multivector(out)
        fig2.savefig("./img2_BlochDiagram")

        # step-3 for counter =3
        qc.ry(np.pi, 0)
        qc.draw(output='mpl',filename='./img3_CircuitDiagram')
        backend = Aer.get_backend('statevector_simulator')
        out = execute(qc,backend).result().get_statevector()
        fig3 = plot_bloch_multivector(out)
        fig3.savefig("./img3_BlochDiagram")

        # step-4 for counter =4
        qc.cx(0,2)
        qc.measure(qr, cr)
        qc.draw(output='mpl',filename='./img4_CircuitDiagram')
        backend = Aer.get_backend('statevector_simulator')
        out = execute(qc,backend).result().get_statevector()
        fig4 = plot_bloch_multivector(out)
        fig4.savefig("./img4_BlochDiagram")


    def showHistogramData(self):
        trials = self.SelectTrials.currentText()
        self.calculateHistogram(int(trials))
        self.histogram.setPixmap(QtGui.QPixmap('./Histogram_'+str(trials)))
        self.histogram.setHidden(False)

    def hideHistogramBatch(self):
        self.histogram.setHidden(True)
        self.pushButton_3.setHidden(True)
        self.SelectTrials.setHidden(True)
        self.stepCountLabel_2.setHidden(True)

    def calculateHistogram(self,trials):
        global qc
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, backend = simulator,shots=trials).result()
        from qiskit.tools.visualization import plot_histogram
        fig = plot_histogram(result.get_counts(qc))
        fig.savefig("./Histogram_"+str(trials))


    def resetDashBoard(self):
        self.circuitDiagram.setPixmap(QtGui.QPixmap())
        self.blochSphere.setPixmap(QtGui.QPixmap('./img0_BlochDiagram'))
        self.atomTransition.setPixmap(QtGui.QPixmap('./Figures_entanglement/img0_AtomConfig'))
        self.hideHistogramBatch()


        self.stepDescription.setText("The qubit states denoted as |up> and |down> are encoded in the NV\n"
            "spin sub-levels m_s = 0 and m_s = -1 respectively. m_s is the \n"
            "spin quantum number which describes angular momentum of an electron.\n"
            "The spins are initialized to |up> state")
        global counter 
        counter = 0
        self.updateCounterStepLabel()

        # TODO - remove histogram and related button when implemented


    def updateCounterStepLabel(self):
        global counter
        self.stepCounterDynamic.setText(str(counter))

    def updateStepDescription(self,stepDescText):
        self.stepDescription.setText(stepDescText)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.inititalizeQbitStates()
    MainWindow.show()
    sys.exit(app.exec_())
