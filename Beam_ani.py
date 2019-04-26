import spidev
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from numpy import sin, cos, cosh, sinh

spi = spidev.SpiDev()
spi.open(0,0)

fig, ax = plt.subplots()
line, = ax.plot([],[],'o', lw=2)
ax.grid()
xdata, ydata = [], []

def analogInput(channel):
    ## Read analog channel
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) <<8) + adc[2]
    return data

def Volts(data):
    ## Convert analog channel to volts
    volts = (data*3.3)/float(1023)
    volts = round(volts,2)
    return volts

def modeShapes(EI_A, rho, L):
    alpha = np.zeros(1) ## Creating only one theoretical mode shape
    R = np.zeros(1)
    wn = np.zeros(1)
    
    x = np.arange(0.0,L,0.01)
    PHI = np.zeros([1,len(x)])
    
    for t in range(len(wn)):
        if t == 0:
            alpha[t] = 0.59686*np.pi
        elif t == 1:
            alpha[t] = 1.49418*np.pi
        R[t] = (cos(alpha[t]) + cosh(alpha[t])) / (sin(alpha[t])+sinh(alpha[t]))
        wn[t] = np.sqrt(EI_A/(rho*L**4)) * alpha[t]**2
        PHI[t] = cosh(alpha[t]*x/L) - cos(alpha[t]*x/L) + R[t]*(sin(alpha[t]*x/L) - sinh(alpha[t]*x/L))
    return PHI

def data_gen(t=0):
    ## Generate real-time time and voltage for each fram 
    cnt = 0
    while True:
        cnt +=1
        x = np.arange(0.0,1,0.01)
        PHI = modeShapes(1,1,1)
        data = analogInput(0)
        tip_displ = Volts(data)*10
        yield x, PHI[0]*tip_displ
        
def init():
    ## Set initial values and plot limits
    ax.set_ylim(-10,10)
    ax.set_xlim(0,1.1)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata,ydata)
    return line,

def run(data):
    ## Update data
    x,y = data
    xdata = x
    ydata = y
    
##    ## Adjust plot boundaries accordingly
##    ymin, ymax = ax.get_ylim()
##    if y >= ymax:
##        ax.set_ylim(ymin,2*ymax)
##        ax.figure.canvas.draw()
##    if y <= ymin:
##        ax.set_ylim(2*ymin, 2*ymax) ## Make sure ymin limit is negative
##        ax.figure.canvas.draw()
##        
    line.set_data(xdata,ydata)
    return line,

## Animate
ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval = .001, repeat = False, init_func = init)
plt.show()
