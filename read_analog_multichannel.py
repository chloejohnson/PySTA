# Partially based on Adafruit library and code written by Tony DiCola (public domain license)


import time
import numpy as np
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



class Measurement():
    '''
        This is an abstract class that contains all options for a specific measurement run. For each new run an object of this class is created 
        and all data is saved as its attribute.
	
	'''
    def __init__(self, fs = 100):
		# The object is created with sampling frequency fs, and empty lists for time and data.
        self.time = []
        self.t_init = time.time()
        self.data = []
        self.fs = fs
        
		
    def setData(self,values):
	# The values for all 8 channels are added to the 'data' attribute of the measurement object
        for i in values:
            self.data.append(values)
        return 	
		
    def setTime(self,t0):
	# The values for the current time (relative to the start time 't_init' is added to the 'time' attribute of the measurement object
		
        self.time.append(t0-self.t_init)
        return 	
		
    		
    
		
    def filterData(self,filter_type):
	# Future work, possible implementation of FIR or IIR filters	
        raise NotImplementedError
    
    def saveData(self,type='time',name='testfile'):
        file = open(name+'.txt','w+')
        if type == 'time':
            file.write('| time | Chann0 | Chann1 | Chann2 | Chann3 | Chann4 | Chann5 | Chann6 | Chann7 |\n')
            for i in range(0,len(self.data)):
                file.write('| {8:.2f} | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |\n'.format(*self.data[i],self.time[i]))
            file.close()
        else:
            file.write('| freq | Chann0 | Chann1 | Chann2 | Chann3 | Chann4 | Chann5 | Chann6 | Chann7 |\n')
            x0 = []
            x1 = []
            x2 = []
            x3 = []
            x4 = []
            x5 = []
            x6 = []
            x7 = []
            for i in self.data:
                x0.append(i[0])
                x1.append(i[1])
                x2.append(i[2])
                x3.append(i[3])
                x4.append(i[4])
                x5.append(i[5])
                x6.append(i[6])
                x7.append(i[7])
            FFT = []
            FFT[0] = list(np.fft.fft(x0))
            FFT[1] = list(np.fft.fft(x1))
            FFT[2] = list(np.fft.fft(x2))
            FFT[3] = list(np.fft.fft(x3))
            FFT[4] = list(np.fft.fft(x4))
            FFT[5] = list(np.fft.fft(x5))
            FFT[6] = list(np.fft.fft(x6))
            FFT[7] = list(np.fft.fft(x7))
            frequency = list(np.linspace(0,self.fs/2,len(self.data)))
            for i in range(0,len(time)):
                file.write('| {8:.2f} | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |\n'.format(*FFT[i],frequency[i]))
            file.close()
        return
        
        
## Hardware configuration
# This is the preferred method. Connect the D_OUT pin of the ADC 3008 to 
# the SPI-designated port on the RaspberryPi 
# Wire the following way:
#
# MCP3008 | RaspberryPi
# ---------------------
# CLK     | SCLK (Pin 11)
# D_OUT   | MISO (Pin 9)
# D_IN    | MOSI (Pin 10)


def data_loop(run):


    SPI_PORT = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE))

    # # Alternative Software configuration
    # CLK  = 11
    # MISO =  9
    # MOSI = 10
    # CS   = 8
    # mcp  = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO,mosi=MOSI)

    print('Reading values from all channels')
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(0,8)))
    print('-'*57)




    
    
    
    T  = 1/run.fs  # time-interval between measurements
    values = [0]*8 # empty list for values

    
    t0 = time.time()
    for i in range(0,8): # loop over all channels
        values[i] = mcp.read_adc(i)*3.3/1024
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    run.setData(values) # send data to measurment object 'run'
    run.setTime(t0) # send time to measurment object 'run'
     
    time.sleep(T-time.time()+t0) # enforce the requested sampling frequency by sleeping for a certain time between each loop
    tf = time.time()
    #print('Elapsed time:', tf	- t0) # this should be very close to the required interval time T=1/fs
	
	
	
    if T-(tf-t0) > 0.01: # check if the application can run in (almost) realtime
        print('----------------------------------------------------------------')
        print('Sampling frequency too large, application cannot run in realtime')
	#	print('----------------------------------------------------------------')

		
    return run
