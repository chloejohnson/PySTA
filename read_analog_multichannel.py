# Partially based on Adafruit library and code written by Tony DiCola (public domain license)


import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



class Measurement():
	'''
		This is an abstract	class that contains all options for a specific measurement run. For each new run an object of this class is created 
		and all data is saved as its attribute.
	
	'''
	def __init__(self, fs = 100, active_channels = [0,1]):
		
		self.data = []
		self.fs = fs
		self.active_channels = active_channels
		
	def setData(self,values):
	# This is done in a loop, where data is continuously written to a measurment object
		for i in values:
			self.data.append(values[i])
		return 	
		
		
	def getData(self):
	# This method returns the data in a structured way, for use in an animation or plot.
		ch0_data = self.data[0:-1:8]
		ch1_data = self.data[1:-1:8]
		# ch2_data = data[2:-1:len(self.active_channels)]
		# ch3_data = data[3:-1:len(self.active_channels)]
		# ch4_data = data[4:-1:len(self.active_channels)]
		# ch5_data = data[5:-1:len(self.active_channels)]
		# ch6_data = data[6:-1:len(self.active_channels)]
		# ch7_data = data[7:-1:len(self.active_channels)]
			
		return ch0_data,ch1_data
		
	def filterData(self,filter_type)
		
		raise NotImplementedError

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




## This loop gets activated whenever the play button is pressed
# Initiallize measurement
run = Measurement(fs = 1, active_channels=[0,1]) #instance of measurement class
T  = 1/userinput_fs

while button_stream == True:
	t0 = time.time()
	for i in range(0,8):
		values[i] = mcp.read_adc(i)
		print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
		run.setData(values)
	time.sleep(T-time.time()+t0)
	if T-time.time()+t0 < 0: # check if the application can run in realtime
		print('----------------------------------------------------------------')
		print('Sampling frequency too large, application cannot run in realtime')
		print('----------------------------------------------------------------')
		button_stream =False
		