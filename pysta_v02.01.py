#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Palash: v2 has button press partially implemented
#### pysta_v02.01.py, plot_in_gui_v2.py

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDateTime, Qt, QTimer, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5.QtGui import QGuiApplication, QPixmap, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from plot_in_gui_v2 import Window
from PyQt5.QtCore import pyqtSlot

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()#INBUILT
        self.show()


        self.createBottomLeftTabWidget()#DEFINED
        label = QLabel(self)
        pixmap = QPixmap('pista.svg')
        label.setPixmap(pixmap)
        q_icon = QIcon(pixmap)
        QApplication.setWindowIcon(q_icon)

        
        fileLabel = QLabel("File Name:")#INBUILT
        fileName = QLineEdit('Test1.txt')
        fileLabel.setBuddy(fileName)#INBUILT
        fsLabel = QLabel("Sampling Frequency [Hz]:")#INBUILT
        samplingFreq = QLineEdit('100')
        fsLabel.setBuddy(samplingFreq)#INBUILT
        shutButton = QPushButton('Shut Down!')
        shutButton.clicked.connect(lambda a:QCoreApplication.instance().quit())
        playButton = QPushButton()
#        Window.played
        playButton.clicked.connect(Window.played)
        playButton.setIcon(QIcon('play.svg'))
        pauseButton = QPushButton()
        pauseButton.setIcon(QIcon('pause.svg'))
        stopButton = QPushButton()
        stopButton.setIcon(QIcon('stop.svg'))
        recordButton = QPushButton()
        recordButton.setIcon(QIcon('record.svg'))

        
        topLayout = QHBoxLayout()#INBUILT
        topLayout.addWidget(fileLabel)
        topLayout.addWidget(fileName)
        topLayout.addStretch(1)#INBUILT
        topLayout.addWidget(fsLabel)
        topLayout.addWidget(samplingFreq)
        topLayout.addStretch(1)#INBUILT
        
        topLayout.addWidget(playButton)
        topLayout.addWidget(pauseButton)
        topLayout.addWidget(stopButton)
        topLayout.addWidget(recordButton)
        topLayout.addWidget(shutButton)
        
        mainLayout = QGridLayout()#INBUILT
        
        mainLayout.addLayout(topLayout, 0, 0)#INBUILT
        mainLayout.addWidget(self.bottomLeftTabWidget, 1, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle("PySTA")#INBUILT
        self.changeStyle('Fusion')#DEFINED

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()#INBUILT
#
    def changePalette(self):
        QApplication.setPalette(self.originalPalette)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()

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

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("It\'s like in the great stories Mr. Frodo. The ones that really mattered. Full of darkness and danger they were, and sometimes you didn't want to know the end. Because how could the end be happy. How could the world go back to the way it was when so much bad happened. But in the end, it's only a passing thing, this shadow. Even darkness must pass. A new day will come. And when the sun shines it will shine out the clearer. Those were the stories that stayed with you. That meant something. Even if you were too small to understand why. But I think, Mr. Frodo, I do understand. I know now. Folk in those stories had lots of chances of turning back only they didn’t. Because they were holding on to something.\n\
                              That there’s some good in this world, Mr. Frodo. And it’s worth fighting for.\n")


        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)
        
        tab3 = QWidget()

        self.matplotlibWidget = Window()

        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(self.matplotlibWidget)
        tab3.setLayout(tab3hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Configuration")
        self.bottomLeftTabWidget.addTab(tab2, "&Plots")
        self.bottomLeftTabWidget.addTab(tab3, "&Animation")
#
#    @pyqtSlot()
#    def played(self):
#        print('PyQt5 button click')
        

if __name__ == '__main__':

    import sys
    w = 700; h = 600

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.setWindowFlags(Qt.Window)
    gallery.resize(w, h)
    gallery.show()
    sys.exit(app.exec_())