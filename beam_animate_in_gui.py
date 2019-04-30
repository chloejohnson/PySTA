"""
UT ASE SPRING 2019
JOHNSON, EITNER, JAIN
ME 369 Final Project

PLOT REAL-TIME TIP-DISPLACEMENTS FROM SENSOR READ IN BY RASPERRY PI

#Ref: https://stackoverflow.com/questions/36162310/how-to-embed-matplotlib-funcanimation-object-within-pyqt-gui?noredirect=1&lq=1
"""
from PyQt5 import QtGui, QtCore,QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation
from matplotlib.figure import Figure
from read_analog_multichannel import data_loop, Measurement
import numpy as np 
from numpy import sin, cos, cosh, sinh


class AniWindow(QtWidgets.QDialog):
    ## Class to create animation object that plots real-time voltage vs time

    def __init__(self):
        super(AniWindow, self).__init__()
        
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
        self.ax.set_ylim(-0.5,0.5)
        self.ax.set_xlim(0,.2)
        self.ax.set_xlabel('X [m]')
        self.ax.set_ylabel('Y [m]')
        self.xdata, self.ydata = [], []
        
        mag = 100 ## Magnify tip displacements
        self.ax.set_title('Real-Time Tip Displacement of Beam, Magnification Factor of ' + str(mag))      
        
        def modeShapes(L):
            ## Generate first mode of a cantilever beam 
            alpha = np.zeros(1)
            R = np.zeros(1)
        
            x = np.arange(0.0,L+0.01,0.01)
            PHI = np.zeros([1,len(x)])
            
            for t in range(len(alpha)):            
                if t == 0:
                    alpha[t] = 0.59686*np.pi
                elif t == 1:
                    alpha[t] = 1.49418*np.pi
               
                R[t] = (cos(alpha[t]) + cosh(alpha[t]))/ (sin(alpha[t]) + sinh(alpha[t]))
                PHI[t] = cosh(alpha[t]*x/L) - cos(alpha[t]*x/L) + R[t]*(sin(alpha[t]*x/L) - sinh(alpha[t]*x/L))
            return PHI
        
        def data_gen(t=0):
            ## Generate real-time tip displacement
            run = Measurement(fs = 10, active_channels=[0,1])                   ## Instance of measurement class

            while True:
                ## Make beam points and mode shape
                L = 15/100 
                x = np.arange(0.0,L+.01,0.01)
                PHI = modeShapes(L)
                
                ## Get real-time tip displacement
                data_loop(run)                                                  ## Adds point to end of vtime and data list
                tip_displ = run.data[-1][1] / 1000                              ## CONVERSION: 1mm / V * 1m/1000mm 
                print(x)
                print(PHI[0]*tip_displ*mag)
                yield x, PHI[0]*tip_displ*mag
        
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
        x, y = data
        self.xdata = x
        self.ydata = y
        self.line.set_data(self.xdata, self.ydata) 
    
        return self.line,        
