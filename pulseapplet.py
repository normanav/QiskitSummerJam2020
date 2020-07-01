import sys
import numpy as np
from PyQt5.QtWidgets import QSlider, QLineEdit, QDoubleSpinBox, QMenu, QRadioButton, QLabel, QSizePolicy, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QComboBox
from PyQt5.QtGui import QIcon, QFont, QCursor, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QDir
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.stats import norm
from qiskit import *
from qiskit.pulse import Play
from qiskit.pulse import pulse_lib
from scipy.optimize import curve_fit

class MainGui(QMainWindow):
    """This is the main window."""
    def __init__(self):
        super(MainGui, self).__init__()
        self.font = QFont('Sans Serif', 12)
        app.setFont(self.font)
        self.title = 'Pulse'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        applet = Applet()
        self.setCentralWidget(applet)
        self.show()

class Applet(QWidget):
    def __init__(self):
        super(Applet, self).__init__()
        self.initapplet()

    def initapplet(self):
        self.objtype = 1
        
        #layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        #title
        title = QLabel("Resonant laser pulses drive optical superpositions\ndepending on the pulse of the power")
        self.layout.addWidget(title, 0,0)
        
        #exper params
        self.params = Experiment(self)
        self.layout.addWidget(self.params, 1,0)
        
        #experiment description
        expdes = QLabel("Rabi and Ramsey experiments are used to\ndetermine the coherence of qubits")
        self.layout.addWidget(expdes, 2, 0)
        
        #energy level pic
        energylevelspic = QLabel()
        energylevelspic.setPixmap(QPixmap(r'./pulseimages/energylevels.png'))
        energylevelspic.setStyleSheet('background-color: white;')
        self.layout.addWidget(energylevelspic, 3, 0)
        
        #contributors
        contrib = QLabel("quid pro quo\nDemo by Liang Li, Jesse Patton\nVictoria Norman, Sridhar Majety")
        self.layout.addWidget(contrib, 4, 0)
        
        #plots
        self.layout.addWidget(self.params.pulseplot, 0, 1, 2, 2)
        self.layout.addWidget(self.params.rabiplot, 2, 1, 3, 1)
        self.layout.addWidget(self.params.ramseyplot, 2, 2, 3, 1)
    
    
class Experiment(QGroupBox):
    def __init__(self, parent):
        QWidget.__init__(self,"Experiment Parameters", parent)
        
        #settings
        self.emitters = ["Diamond NV", "Diamond SiV", "SiC Vacancy", "SiC Divacancy", "Quantum Dot"]
        self.freqs = dict(zip(self.emitters,(637, 738, 918, 1042, 900)))
        self.pulseparams = ['Pulse Energy', 'Pulse Width', 'Max Delay']
        self.experiments = ["Rabi", "Ramsey"]
        mms = ['min', 'max', 'step']
        self.minmaxstep = {#min max step size for slider conversion position to value
            'Pulse Energy'  : dict(zip(mms,(0, 10, 0.1))),
            'Pulse Width': dict(zip(mms,(0, 10, 0.1))),
            'Max Delay': dict(zip(mms,(0, 500, 1)))
            }
        
        #qiskit backend
        self.qkback = QiskitBackend()
        #plots
        self.pulseplot = PulsePlot()
        self.rabiplot = RabiPlot()
        self.ramseyplot = RamseyPlot()
        
        #layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumWidth(400)
        
        #emitter section
        emitterbox = QGroupBox("Emitter Type")
        layout.addWidget(emitterbox)
        emitterlayout = QVBoxLayout()
        emitterbox.setLayout(emitterlayout)
        self.emittercombobox = QComboBox()
        
        for item in self.emitters:
            self.emittercombobox.addItem(item)
        self.emittercombobox.currentIndexChanged.connect(self.on_emitterchange)
        emitterlayout.addWidget(self.emittercombobox)
        
        #laser
        laserlayout = QGridLayout()
        laserlayout.addWidget(QLabel("Ultrafast Laser"),0,0)
        self.wavelengthlabel = QLabel("\u03BB = {} nm".format(self.wavelength))
        laserlayout.addWidget(self.wavelengthlabel, 0,1)
        emitterlayout.addLayout(laserlayout)
        
        #pulse slider section
        pulsebox = QGroupBox("Pulse Parameters")
        layout.addWidget(pulsebox)
        pulselayout = QGridLayout()
        pulsebox.setLayout(pulselayout)
        self.sliders = {}
        self.valuelabels = {}
        for row, item in enumerate(self.pulseparams):
            pulselayout.addWidget(QLabel(item),row,0)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            mms = self.minmaxstep[item]
            slider.setMaximum(int((mms['max']-mms['min'])/mms['step']))
            slider.setValue(10)
            slider.valueChanged.connect(self.on_sliders)
            pulselayout.addWidget(slider, row, 1)
            self.sliders[item] = slider
            label = QLabel('')
            pulselayout.addWidget(label, row, 2)
            self.valuelabels[item] = label
        label = QLabel('')
        pulselayout.addWidget(label, 3, 0, 1, 3)
        self.valuelabels['Pulse Power'] = label
        self.updatelabels()
        
        #Experiment type
        typebox = QGroupBox("Experiment Type")
        layout.addWidget(typebox)
        typelayout = QHBoxLayout()
        typebox.setLayout(typelayout)
        self.exptypebuttons = {}
        for item in self.experiments:
            button = QRadioButton(item)
            button.toggled.connect(self.on_expchange)
            button.toggled.connect(self.update_pulseplot)
            typelayout.addWidget(button)
            self.exptypebuttons[item] = button
        list(self.exptypebuttons.items())[0][1].click()
        
        self.runbutton = QPushButton('Run Experiments')
        layout.addWidget(self.runbutton)
        self.runbutton.clicked.connect(self.on_run)
        
        self.update_pulseplot()
        
    @property
    def emitter(self): 
        return self.emittercombobox.currentText()

    @property
    def wavelength(self): 
        return self.freqs[self.emitter]
    
    @property
    def exptype(self):
        tpe = None
        for key, button in self.exptypebuttons.items():
            if button.isChecked():
                tpe = key
                break
        return tpe

    @property
    def energy(self): 
        mms = self.minmaxstep['Pulse Energy']
        pos = self.sliders['Pulse Energy'].value()
        return mms['min'] + pos * mms['step']

    @property
    def width(self):
        mms = self.minmaxstep['Pulse Width']
        pos = self.sliders['Pulse Width'].value()
        return mms['min'] + pos * mms['step']

    @property
    def delay(self):
        mms = self.minmaxstep['Max Delay']
        pos = self.sliders['Max Delay'].value()
        return mms['min'] + pos * mms['step']
    
    @property
    def power(self):
        try:
            return self.energy / self.width
        except:
            return 0
    
    def on_sliders(self):
        self.updatelabels()
        self.update_pulseplot()
        
    def updatelabels(self):
        self.valuelabels['Pulse Power'].setText("Pulse Power = {:.2f} mW".format(self.power))
        self.valuelabels['Pulse Energy'].setText("{:.1f} fJ".format(self.energy))
        self.valuelabels['Pulse Width'].setText("{:.1f} ps".format(self.width))
        self.valuelabels['Max Delay'].setText("{} ps".format(self.delay))
    
    def on_emitterchange(self):
        self.wavelengthlabel.setText("\u03BB = {} nm".format(self.wavelength))

    def on_expchange(self):
        self.update_pulseplot()
    
    def update_pulseplot(self):
        self.pulseplot.plot(self.energy, self.width, self.delay, self.exptype)
    
    def on_run(self):
        results = runexp(self.qkback, self.energy, self.width, self.delay)
        self.rabiplot.plot(*results['rabi'])
        self.ramseyplot.plot(*results['ramsey'])


class PlotCanvas(FigureCanvas): #this creates a matplotlib canvas and defines some plotting aspects
    def __init__(self, parent=None, fig=None):
        if fig is not None:
            self.fig = fig
        else:
            self.fig = Figure()
            self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
    
class PulsePlot(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        self.setLayout(QVBoxLayout())
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.canvas = PlotCanvas(self) 
        self.layout().addWidget(self.canvas)
        
    def plot(self, energy, width, delay, exptype, center=20):
        ax = self.canvas.fig.axes[0]
        ax.clear()
        x1 = np.arange(center-3*width, center+3*width, 0.1)
        y1 = norm.pdf(x1, center, width/2) * energy
        ax.plot(x1, y1)
        ax.fill_between(x1, y1, alpha=0.3)
        ax.set_xlim(0, 40)
        if exptype == 'Ramsey':
            x2 = np.arange(delay+center-3*width, delay+center+3*width, 0.1)
            y2 = norm.pdf(x2, center + delay, width/2) * energy
            ax.plot(x2,y2)
            ax.fill_between(x2,y2,alpha=0.3)
            ax.set_xlim(0, 500)
        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Power')
        ax.set_yticklabels([])
        ax.set_title('Laser Pulse(s)')
        self.canvas.draw()
        
class RamseyPlot(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        self.setLayout(QVBoxLayout())
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.canvas = PlotCanvas(self) 
        self.layout().addWidget(self.canvas)
        
    def plot(self, x, y):
        ax = self.canvas.fig.axes[0]
        ax.clear()
        #plot
        ax.scatter(x, y, color='black')
        ax.set_xlim(0, np.max(x))
        ax.set_title("Ramsey Experiment Results")
        ax.set_xlabel('Delay between X90 pulses [$f$s]')
        ax.set_ylabel('Probability of qubit being |0\u232A')
        self.canvas.draw()
        
class RabiPlot(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        self.setLayout(QVBoxLayout())
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.canvas = PlotCanvas(self) 
        self.layout().addWidget(self.canvas)
        
    def plot(self, x, y):
        ax = self.canvas.fig.axes[0]
        ax.clear()
        ax.scatter(x, y, color='black')
        ax.set_xlabel("Power^1/2 [mW]")
        ax.set_ylabel("Probablity of qubit being |0\u232A")
        ax.set_title("Rabi Experiment Results")
        self.canvas.draw()

def runexp(qkback, energy, width, delay):
    results = {}
    #drive params
    drive_sigma_us = width/(2 * 10)
    drive_samples_us = drive_sigma_us*2       
    drive_sigma = get_closest_multiple_of_16(drive_sigma_us * qkback.us / qkback.dt)      
    drive_samples = get_closest_multiple_of_16(drive_samples_us * qkback.us / qkback.dt)  
    drive_amp = energy/10
    scale_factor = 1
    
    #Rabi
    # Rabi experiment parameters
    num_rabi_points = 50
    # Drive amplitude values to iterate over: 50 amplitudes evenly spaced from 0 to 1
    drive_amp_min = 0
    drive_amp_max = 1 #input from 0 to 1
    drive_amps = np.linspace(drive_amp_min, drive_amp_max, num_rabi_points)
    rabi_schedules = []
    for drive_amp in drive_amps:
        rabi_pulse = pulse_lib.gaussian(duration=drive_samples, amp=drive_amp, 
                                        sigma=drive_sigma, name=f"Rabi drive amplitude = {drive_amp}")
        this_schedule = pulse.Schedule(name=f"Rabi drive amplitude = {drive_amp}")
        this_schedule += Play(rabi_pulse, qkback.drive_chan)
        # Reuse the measure instruction from the frequency sweep experiment
        this_schedule += qkback.measure << this_schedule.duration
        rabi_schedules.append(this_schedule)
        
    # Assemble the schedules into a Qobj
    num_shots_per_point = 1024
    test = qkback.center_frequency_Hz
    rabi_experiment_program = assemble(rabi_schedules,
                                        backend=qkback.backend,
                                        meas_level=1,
                                        meas_return='avg',
                                        shots=num_shots_per_point,
                                        schedule_los=[{qkback.drive_chan: test}] * num_rabi_points)
    # print(job.job_id())
    job = qkback.backend.run(rabi_experiment_program)
    #job_monitor(job)
    rabi_results = job.result(timeout=120)
    
    #graph of Probability of being in |1> state vs. Power^1/2
    rabi_values = []
    for i in range(num_rabi_points):
        # Get the results for `qubit` from the ith experiment
        rabi_values.append(rabi_results.get_memory(i)[qkback.qubit]*scale_factor)
    rabi_values = np.real(baseline_remove(rabi_values))
    prob = ((rabi_values / np.min(rabi_values)) + 1) / 2
    
    rabix = drive_amps / np.sqrt(drive_samples_us)
    results['rabi'] = (rabix, prob)
    
    #ramsey
    def fit_function(x_values, y_values, function, init_params):
        fitparams, conv = curve_fit(function, x_values, y_values, init_params)
        y_fit = function(x_values, *fitparams)
        return fitparams, y_fit
    
    fit_params, y_fit = fit_function(drive_amps,
                                     rabi_values,
                                     lambda x, A, B, drive_period, phi: (A*np.cos(2*np.pi*x/drive_period - phi) + B),
                                     [3, 0.1, 0.5, 0]),
    
    drive_period = fit_params[2] # get period of rabi oscillation
    
    #Finding the value of pi pulse and x90 pulse (half pi pulse)
    pi_amp = abs(drive_period / 2)
    halfpi_amp = pi_amp/2
    
    pi_pulse = pulse_lib.gaussian(duration=drive_samples,
                                amp=pi_amp, 
                                sigma=drive_sigma,
                                name='pi_pulse')
    halfpi_pulse = pulse_lib.gaussian(duration=drive_samples,
                                amp=halfpi_amp, 
                                sigma=drive_sigma,
                                name='halfpi_pulse')
    
    # Ramsey experiment parameters
    time_max_us = delay*4/1000  #frontend 1800 fs
    time_step_us = 0.025 #frontend 2.5 fs
    times_us = np.arange(0.1, time_max_us, time_step_us)
    # Convert to units of dt
    delay_times_dt = times_us * qkback.us / qkback.dt

    # Drive parameters
    # The drive amplitude for pi/2 is simply half the amplitude of the pi pulse
    ram_drive_amp = pi_amp / 2
    # x_90 is a concise way to say pi_over_2; i.e., an X rotation of 90 degrees
    x90_pulse = pulse_lib.gaussian(duration=drive_samples,
                                amp=ram_drive_amp, 
                                sigma=drive_sigma,
                                name='x90_pulse')
    
    # create schedules for Ramsey experiment 
    ramsey_schedules = []
    for dely in delay_times_dt:
        this_schedule = pulse.Schedule(name=f"Ramsey delay = {delay * dt / us} us")
        this_schedule |= Play(x90_pulse, qkback.drive_chan)
        this_schedule |= Play(x90_pulse, qkback.drive_chan) << int(this_schedule.duration + dely)
        this_schedule |= qkback.measure << int(this_schedule.duration)
        ramsey_schedules.append(this_schedule)
    
    # Execution settings
    num_shots = 256
    detuning_MHz = 2 
    ramsey_frequency = round(qkback.center_frequency_Hz + detuning_MHz * MHz, 6) # need ramsey freq in Hz
    ramsey_program = assemble(ramsey_schedules,
                                backend=qkback.backend,
                                meas_level=1,
                                meas_return='avg',
                                shots=num_shots,
                                schedule_los=[{qkback.drive_chan: ramsey_frequency}]*len(ramsey_schedules)
                                )
    job = qkback.backend.run(ramsey_program)
    ramsey_results = job.result(timeout=120)
    
    #Ramsey experiment: Probability vs. time delay
    ramsey_values = []
    for i in range(len(times_us)):
        ramsey_values.append(ramsey_results.get_memory(i)[qkback.qubit]*scale_factor)
    probramsey = (np.real(ramsey_values) / np.min (np.real(ramsey_values)) + 1) / 2
    x = times_us
    results['ramsey'] = (x,probramsey)

    return results
        
        
        
        

class QiskitBackend():
    def __init__(self):
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
        self.backend = provider.get_backend('ibmq_armonk')
        self.backend_config = self.backend.configuration()
        assert self.backend_config.open_pulse, "Backend doesn't support Pulse"
        self.dt = self.backend_config.dt
        backend_defaults = self.backend.defaults()
        
        # unit conversion factors -> all backend properties returned in SI (Hz, sec, etc)
        self.GHz = 1.0e9 # Gigahertz
        self.MHz = 1.0e6 # Megahertz
        self.us = 1.0e-6 # Microseconds
        self.ns = 1.0e-9 # Nanoseconds

        self.qubit = 0

        #the estimated qubit frequency.
        self.center_frequency_Hz = backend_defaults.qubit_freq_est[self.qubit] # The default is given in Hz
        
        # Find out which group of qubits need to be acquired with this qubit
        self.meas_map_idx = None
        for i, measure_group in enumerate(self.backend_config.meas_map):
            if self.qubit in measure_group:
                self.meas_map_idx = i
                break
        assert self.meas_map_idx is not None, f"Couldn't find qubit {self.qubit} in the meas_map!"
        
        inst_sched_map = backend_defaults.instruction_schedule_map
        self.measure = inst_sched_map.get('measure', qubits=self.backend_config.meas_map[self.meas_map_idx])
        
        ### Collect the necessary channels
        self.drive_chan = pulse.DriveChannel(self.qubit)
        self.meas_chan = pulse.MeasureChannel(self.qubit)
        self.acq_chan = pulse.AcquireChannel(self.qubit)
        
def get_closest_multiple_of_16(num):
    # samples need to be multiples of 16
    return int(num + 8 ) - (int(num + 8 ) % 16)

# center data around 0
def baseline_remove(values):
    return np.array(values) - np.mean(values)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainGui()
    sys.exit(app.exec_())
