#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
############################# UT ASE SPRING 2019 ##############################
########################### JOHNSON, EITNER, JAIN #############################
############################ ME 369 Final Project #############################
################ PySTA - Python Standard for Test and Analysis ################
###############################################################################
###################### (c) GNU GENERAL PUBLIC LICENSE #########################
########################## Version 3, 29 June 2007 ############################
###############################################################################

from PyQt5.QtCore import QDateTime, Qt, QTimer, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtGui import QGuiApplication, QPixmap, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from plot_in_gui import Window #Import class from accompanying file
from beam_animate_in_gui import AniWindow #Import class from accompanying file


reset_button = "global" #Reset Button press action transcends widgets
		
class PySTA(QDialog): #Class containing GUI structure
    def __init__(self, parent=None):
        super(PySTA, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.show()
        self.fs = 10 #Default sampling frequency in Hz.
        self.N_samples = 100 #Default sampling frequency in Hz.
        
############## Display compatibility warning popup ############################
        msgBox = QMessageBox() 
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("PySTA v8")
        msgBox.setText("This applicaton runs on Raspberry Pi.")
        label = QLabel(self)
        pixmap = QPixmap('pista.svg')
        label.setPixmap(pixmap)
        q_icon = QIcon(pixmap)
        QApplication.setWindowIcon(q_icon)
###############################################################################
        
############## Setting top panel widgets ######################################
        fileLabel = QLabel("File Name:") 
        fileName = QLineEdit('Test1.txt')
        fileLabel.setBuddy(fileName)
        fsLabel = QLabel("Sampling Frequency [Hz]:")
        self.samplingFreq = QLineEdit('10') #Default sampling frequency in Hz. 
        self.samplingFreq.textChanged.connect(self.setFs) #Detects text update
        fsLabel.setBuddy(self.samplingFreq)
        nSamplesLabel = QLabel("Number of Samples:")
        self.nSamples = QLineEdit('100') #Default sampling frequency in Hz. 
        self.nSamples.textChanged.connect(self.setNs) #Detects text update
        nSamplesLabel.setBuddy(self.nSamples)
        resetButton = QPushButton('Reset') #Reads user inputs on top panel \n
		                                   #Also resets plots when stop pressed
        shutButton = QPushButton('Shut Down!') #Safely exit from PySTA
        shutButton.clicked.connect(lambda a:QCoreApplication.instance().quit())
###############################################################################

############## Inserting top panel widgets ####################################        
        topLayout = QHBoxLayout()
        topLayout.addWidget(fileLabel)
        topLayout.addWidget(fileName)
        topLayout.addStretch(1)
        topLayout.addWidget(fsLabel)
        topLayout.addWidget(self.samplingFreq)
        topLayout.addStretch(1)
        topLayout.addWidget(nSamplesLabel)
        topLayout.addWidget(self.nSamples)
        topLayout.addStretch(1)
        topLayout.addWidget(resetButton)
        topLayout.addWidget(shutButton)
###############################################################################

############## Inserting main panel widgets ###################################       
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(topLayout, 0, 0)
        self.setLayout(self.mainLayout)
        self.createBottomWidget()
        self.mainLayout.addWidget(self.bottomWidget, 1, 0)
        self.fs = float(self.samplingFreq.text())
        self.N_samples = float(self.nSamples.text())
        msgBox.exec();
        resetButton.clicked.connect(self.proceed)
        self.setWindowTitle("PySTA")
        self.changeStyle('Fusion')
###############################################################################
    
############## Method to read user inputs and reset plots ######################
    def proceed(self):
        reset_button = 1
        animation = Window(channel = 0,fs = self.fs, N_samples = self.N_samples)
        animation.animate()
        self.createBottomWidget()
        self.mainLayout.addWidget(self.bottomWidget, 1, 0)
        self.fs = float(self.samplingFreq.text())
        self.N_samples = float(self.nSamples.text())
###############################################################################
        
############## Method to read and pass sampling frequency #####################
    def setFs(self):
        self.fs = float(self.samplingFreq.text())
###############################################################################

############## Method to read and pass number of samples ######################
    def setNs(self):
        self.N_samples = float(self.nSamples.text())
###############################################################################


############## Styling methods ################################################
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(self.originalPalette)
###############################################################################


############## Method to assign and add objects to main panel##################
    def createBottomWidget(self):
        self.bottomWidget = QTabWidget()

        tab1 = QWidget()
        checkBox1 = QCheckBox("Channel 0")
        checkBox2 = QCheckBox("Channel 1")
        checkBox3 = QCheckBox("Channel 2")
        checkBox1.setChecked(True)

        tab1contents = QVBoxLayout()
        tab1contents.addWidget(checkBox1)
        tab1contents.addWidget(checkBox2)
        tab1contents.addWidget(checkBox3)
        tab1.setLayout(tab1contents)
###############################################################################

############## Adds plot objects in second tab ################################
        tab2 = QWidget()
        self.matplotlibWidget1 = Window(channel = 0,fs = self.fs, N_samples = self.N_samples)
        self.matplotlibWidget2 = Window(channel = 1, fs=self.fs, N_samples = self.N_samples)
        tab2hbox = QVBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(self.matplotlibWidget1)
        tab2hbox.addWidget(self.matplotlibWidget2)
        tab2.setLayout(tab2hbox)
###############################################################################

############## Adds animate object in second tab ##############################        
        tab3 = QWidget()
        self.matplotlibWidget = AniWindow(fs = self.fs, N_samples = self.N_samples)
        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(self.matplotlibWidget)
        tab3.setLayout(tab3hbox)

        self.bottomWidget.addTab(tab1, "&Configuration")
        self.bottomWidget.addTab(tab2, "&Plots")
        self.bottomWidget.addTab(tab3, "&Animation")
###############################################################################
    

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = PySTA()
    gallery.setWindowFlags(Qt.Window)
    gallery.show()
    sys.exit(app.exec_())
