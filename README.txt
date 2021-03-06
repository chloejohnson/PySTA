Created 04/26/2019
Group Members: Marc Eitner, Palash Jain, Chloe Johnson

The objective of this project is to replicate an instrument interface such as 
LabView using Python and a Raspberry Pi, making data collection for small 
experiments more portable, affordable, and user-friendly. 

Specifically, the project aims to measure the accelerations and displacements 
of a cantilever beam, read them into a GUI that that allows simple tasks such 
as filtering or live-streaming the data to create frequency and time-domain 
plots. One of these options will be to create a real time animation of the 
displacement of the beam.
  
CODES:


- ANIMATION:
    > plot_in_gui.py: Plots the real-time voltage input versus time of a sensor. Creates a class, Window(channel = #, fs = #, N_samples = #), which is a function of the channel voltage to be plotted, the sampling frequency, and the number of samples to be read.
    > beam_animate_in_gui.py: Animates a 1D beam in its first mode shape from given voltage input of tip displacement. Creates a class, AniWindow(fs = #, N_samples = #), which is a function of the sampling frequency and the number of               samples to be read.).


- RASPBERRY PI INTERFACE:
    > The analog data is read by the RaspberryPi through an Analog-Digital-Converter (ADC) of type MCP3008, which allows 8 channels to be read with a 10bit resolution. In its current configuration, the measurement range of the analog input is [0-3.3V DC].
    > read_analog_multichannel: This code contains a class definition and a function. The 'Measurement' class contains a set of methods such as filtering and data input and output. It also contains the SPI communication between the RaspberryPi and the Analog-Digital-Converter (ADC). At the beginning of each test, a new object of the class 'Measurements' is created. All measured data as well as the corresponding time vector is stored in it. The data is then called by several other plotting/animation functions. The function 'data_loop' measures the current value from the ADC (all 8 channels) and then adds these values to the 'data' attribute of the current 'Measurement'-class object.
     

- GUI
    > pysta.py: This file encompasses the design of the GUI. Layout, tabs, widgets and options for user inputs are handled here. Dependencies and feedback of reset and shut buttons are also implemented. Matplotlib widgets returned by plot_in_gui and beam_animate_in_gui are added to the respective tabs. 
    > *.svg: accessories (images for GUI buttons, etc.)
    

- txt files are sample outputs of measured data
