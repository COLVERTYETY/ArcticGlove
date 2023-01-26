import numpy as np
import pyqtgraph as pg
from collections import deque
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time
import serial 
import signal
import sys

#  on click on widget get x,y coordinates
def SignalHandler(sig, frame):
    print("SignalHandler")

    app.quit()
    
    sys.exit(0)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        

        self.gain = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.gain.setMinimum(0)
        self.gain.setMaximum(30)
        self.gain.setValue(0)

        self.gain.setTickInterval(1)
     
        self.treshold = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.treshold.setMinimum(0)
        self.treshold.setMaximum(20)
        self.treshold.setValue(0)
        self.treshold.setTickInterval(1)
        self.treshold.valueChanged.connect(self.tresholdChanged)

        self.gain_label = QtWidgets.QLabel()
        self.gain_label.setText("Gain: " + str(self.gain.value()))
        
        self.treshold_label = QtWidgets.QLabel()
        self.treshold_label.setText("Treshold: " + str(self.treshold.value()))

        self.graphWidget.setBackground('w')
        self.graphWidget.scene().sigMouseClicked.connect(self.mouseClicked)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.gain)
        layout.addWidget(self.gain_label)
        layout.addWidget(self.treshold)
        layout.addWidget(self.treshold_label)

        self.gain.valueChanged.connect(self.gainChanged)
        self.setLayout(layout)
        # Create a central widget for the layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Set the window title
        self.setWindowTitle("Arctic Glove")

        #Add a widget to modify the value of a variable
        # self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(100)
        # self.slider.setValue(50)
        # self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        # self.slider.setTickInterval(10)
        # self.slider.valueChanged.connect(self.sliderChanged)
        # self.slider.setFixedWidth(200)
        # self.slider.setFixedHeight(50
        # self.data_line =  self.graphWidget.plot(self.delegate.times, self.delegate.vals, pen=pen)

        # self.timer2 = QtCore.QTimer()
        # self.timer2.setInterval(10)
        # self.timer2.timeout.connect(self.readByte)
        # self.timer2.start()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.ser = serial.Serial('/dev/ttyUSB0', 250000, timeout=0.1)
        self.sync = False
        self.calibration = []
        #TO DEFINE
        self.cols = 9
        self.rows = 9

        self.cells = self.cols*self.rows
        self.buffer = np.zeros(self.cells)
        self.mean = 10000
        self.std = 10000
    
    def tresholdChanged(self):
        treshold = self.treshold.value()
        self.treshold_label.setText("Treshold: " + str(treshold))
        print(treshold)

    def gainChanged(self):
        gain = self.gain.value()
        self.gain_label.setText("Gain: " + str(gain))
        

    def mouseClicked(self, event):
        self.calibration = []
        print("Mouse clicked at: ", event.scenePos())

    def readSync(self):
        while(not self.sync):
            data = self.ser.readline()
            if len(data) < 3:
                print("No sync")
                continue
            buffer = data.split(b":")
            if len(buffer) ==5:
                self.cols = int(buffer[1])
                self.rows = int(buffer[3])
                self.cells = self.cols*self.rows
                self.sync = True
                print(self.cols, self.rows, self.cells)
                for i in range(5):
                    print(buffer[i])
                print("Synced")
                return
    
    def readString(self):
        data = self.ser.readline()
        if len(data) >= self.cells:
            data = data.decode("utf-8")
            data = data.split(",")
            try:
                data = [int(i) for i in data]
            except:
                self.sync = False
                self.readSync()
            # print(data)
            if len(data)==self.cells:
                self.buffer = np.array(data)

    def readByte(self):
        data = self.ser.read(self.cells+2)
        if len(data)==self.cells+2:
            lowbyteMin = data[1]
            highbyteMin = data[0]
            min = int(highbyteMin)<<8 + int(lowbyteMin)

            self.buffer = np.zeros(self.cells)
            for i in range(self.cells):
                self.buffer[i] = data[i+2] + min

        else:
            print("No data", data)
            # self.sync = False
            # self.readSync()
            # self.ser.write(b"s")

    def setup(self):
        print("Setup")
        # while not self.sync:
        #     print("Syncing")
        self.readSync()
        self.ser.write(str(self.gain.value()).encode())

    def update_plot_data(self):
        gain_bytes = str(self.gain.value()).encode()
        self.ser.write(gain_bytes)
        #self.ser.write(b"s")
        # self.readByte()
        self.readString()
        #  reashaep the data
        self.buffer = self.buffer.reshape(self.rows, self.cols)
        #  plot the data*
        # print(self.buffer.shape)
        temp = self.buffer
        if len(self.calibration)<80:
            self.calibration.append(self.buffer)
            self.mean = np.mean(np.array(self.calibration), axis=0)
            self.std = np.std(np.array(self.calibration), axis=0)
            if len(self.calibration)%10==0:
                print(len(self.calibration))
  
        # temp = np.clip(temp, 0, 1000)
        temp = temp - self.mean
        print(temp)
        temp[temp<self.treshold.value()] = 0

        #disable auto levels

        image = pg.ImageItem(temp, autoLevels=False, autoRange=False, autoHistogramRange=False, levels=(0, 30))
        self.graphWidget.plotItem.clear()
        self.graphWidget.plotItem.addItem(image)
        # self.graphWidget.setImage(self.buffer, autoLevels=False, autoRange=False, autoHistogramRange=False, levels=(0, 1000))
        


#attach the signal
signal.signal(signal.SIGINT, SignalHandler)



app = QtWidgets.QApplication([])
w = MainWindow()
w.setup()
w.show()
app.exec_()
# dev.disconnect()s
while True:
    # if dev.waitForNotifications(1.0):
        # handleNotification() was called
        # continue
    # print("Waiting...")
    pass