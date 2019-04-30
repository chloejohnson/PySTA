Created 04/26/2019
Group Members: Marc Eitner, Palash Jain, Chloe Johnson
  Full Name: Marc Eitner
  EID: mae2888

  Full Name: Palash Jain
  EID: pj5453

  Full Name: Chloe Johnson
  EID: cmj2855

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
    > plot_in_gui.py: Plots the real-time voltage input versus time of a sensor. Creates a class, Window(channel = #, fs = #),        which is a function of the channel voltage to be plotted and the sampling frequency.
    > beam_animate_in_gui.py: Animates a 1D beam in its first mode shape from given voltage input of tip displacement. Creates        a class, AniWindow().

- RASPBERRY PI INTERFACE:
    > read_analog_multichannel: This code contains the measurement class, which contains a set of methods such as filtering         and data input and output. It also contains the SPI communication between the RaspberryPi and the Analog-Digital-             Converter.

- GUI
    > pysta_v01.01.py: design of the GUI, dependencies and feedback of button press actions not implemented.
    > *.svg: accessories (images for GUI buttons, ect.)
