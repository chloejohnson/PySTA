import spidev
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation


spi = spidev.SpiDev()
spi.open(0,0)

y = []
t = []
fig, ax = plt.subplots()
line, = ax.plot([],[], lw=1)
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
    
def data_gen(t=0):
    ## Generate real-time time and voltage for each fram 
    cnt = 0
    while True:
        cnt +=1
        t += 0.1
        data = analogInput(0)
        print(Volts(data))
        yield t, Volts(data)
        
def init():
    ## Set initial values and plot limits
    ax.set_ylim(0,1)
    ax.set_xlim(0,5)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata,ydata)
    return line,

def run(data):
    ## Update data
    t,y = data
    xdata.append(t)
    ydata.append(y)
    
    ## Adjust plot boundaries accordingly
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    if y >= ymax:
        ax.set_ylim(ymin,2*ymax)
        ax.figure.canvas.draw()
    if y <= ymin:
        ax.set_ylim(2*ymin, 2*ymax) ## Make sure ymin limit is negative
        ax.figure.canvas.draw()
        
    line.set_data(xdata,ydata)
    return line,

## Animate
ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval = .001, repeat = False, init_func = init)
plt.show()