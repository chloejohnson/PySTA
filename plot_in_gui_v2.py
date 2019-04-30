#Ref: https://stackoverflow.com/questions/36162310/how-to-embed-matplotlib-funcanimation-object-within-pyqt-gui?noredirect=1&lq=1

from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from matplotlib.figure import Figure

class Window(QtWidgets.QDialog): #or QtGui.QWidget ???
#    @pyqtSlot()
    def __init__(self):
        super(Window, self).__init__()
#        self.fig = plt.figure()
#        self.fig = Figure(figsize=(5,4),dpi=100)
        self.button = QtWidgets.QPushButton('Animate')
        self.button.clicked.connect(self.animate)
#        if playState == 1:
#            print('Yes!')
#        self.animate
#        self.ax.hold(False)  # discards the old graph
        self.fig = Figure(figsize=(5,4),dpi=100)
        self.canvas = FigureCanvas(self.fig)
        
        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    
#    @pyqtSlot()
    def played(self):
#        self.animate()
        print('PyQt5 button click')
    
    def data_gen(t=0):
        cnt = 0
        while cnt < 500:
            cnt += 1
            t += 0.1
            yield t, -5*t
        
    def animate(self):
        def data_gen(t=0):
            cnt = 0
            while cnt < 500:
                cnt += 1
                t += 0.1
                yield t, -5*t
        self.ax = self.fig.add_subplot(111)  # create an axis
        self.line, = self.ax.plot([], [],'o', lw=2)
        self.ax.grid()
        self.xdata, self.ydata = [], []
#        self.ax.hold(False)  # discards the old graph
#        self.circle = Circle((0,0), 1.0)
#        self.ax.add_artist(self.circle)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, 10)
#        self.ax.set_xlim([0,10])
#        self.ax.set_ylim([-2,2])

        self.anim = animation.FuncAnimation(self.fig, self.animate_loop, data_gen, blit=False, interval=.000,
                              repeat=False)#, init_func=init)
#        animation.FuncAnimation(self.fig,self.animate_loop,frames=10,interval=100,repeat=False,blit=False)
#        plt.show()
        self.canvas.draw()

    def animate_loop(self,data):
    # update the data
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
    
        if t >= xmax:
            self.ax.set_xlim(xmin, 2*xmax)
            self.ax.figure.canvas.draw()
        if y >= ymax:
            self.ax.set_ylim(ymin,2*ymax)
            self.ax.figure.canvas.draw()
        if y <= ymin:
            self.ax.set_ylim(2*ymin,ymax)
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)
    
        return self.line,

#w = Window()
#w.show()
#plt.show()