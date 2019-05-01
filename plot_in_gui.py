"""
UT ASE SPRING 2019
JOHNSON, EITNER, JAIN
ME 369 Final Project

PLOT REAL-TIME VOLTAGES FROM SENSORS READ IN BY RASPERRY PI

#Ref: https://stackoverflow.com/questions/36162310/how-to-embed-matplotlib-funcanimation-object-within-pyqt-gui?noredirect=1&lq=1
"""
from PyQt5 import QtGui, QtCore,QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation
from matplotlib.figure import Figure
from read_analog_multichannel import data_loop, Measurement


class Window(QtWidgets.QDialog):
    ## Class to create animation object that plots real-time voltage vs time

    def __init__(self, channel,fs,N_samples):
        super(Window, self).__init__()
        self.channel = channel
        self.fs = fs
        self.N_samples = N_samples
        
        ## Animation figure
        self.fig = Figure(figsize=(5,4),dpi=100)
        self.canvas = FigureCanvas(self.fig)
        
        ## Animate button
        self.button = QtWidgets.QPushButton('Animate')
        self.button.clicked.connect(self.animate)
        
        ## Set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def animate(self):
        ## Animation figure settings
        self.ax = self.fig.add_subplot(111) 
        self.line, = self.ax.plot([], [], lw=1)
        self.ax.grid()
        self.ax.set_ylim(-5,5)
        self.ax.set_xlim(0,10)
        self.ax.set_xlabel('Time [sec]')
        self.ax.set_ylabel('Voltage Out [V]')
        self.ax.set_title('Channel ' + str(self.channel))
        self.xdata, self.ydata = [], []
        
        def data_gen(t=0):
            ## Generate real-time time and voltage for each frame
            run = Measurement(fs = self.fs, active_channels=[0,1]) ## Instance of measurement class
            cnt = 0
            while cnt < self.N_samples:
                cnt = cnt+1
                data_loop(run) ## Adds point to end of vtime and data list
                yield run.time[-1], run.data[-1][self.channel]
        
        ## ~Run animation functioion~
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop, data_gen, blit=True,
                                            interval=.001, repeat=False, init_func=self.initial)
        ## Update figure in GUI
        self.canvas.update()
   
   
    def initial(self):
        ## Clear data
        self.line.set_data([],[])
        
        return self.line,
       
        
    def animate_loop(self,data):
        ## Update data
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        
        ## Adjust plot boundaries accordingly
        if t >= xmax:
            self.ax.set_xlim(xmin, 2*xmax)
            self.ax.figure.canvas.draw()
        if y >= ymax:
            self.ax.set_ylim(ymin,2*ymax)
            self.ax.figure.canvas.draw()
        if ymin < 0: ## Make sure ymin limit is negative if this is used
            if y <= ymin:
                self.ax.set_ylim(2*ymin,ymax) 
                self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata) 
    
        return self.line,        
