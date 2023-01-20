import numpy as np
import pyqtgraph as pg
from collections import deque
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time
import serial 


#  on click on widget get x,y coordinates
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        # widget for slider
        self.graphWidget.setBackground('w')
        self.graphWidget.scene().sigMouseClicked.connect(self.mouseClicked)
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
        self.cols = 12
        self.rows = 12
        self.cells = 21*12
        self.buffer = np.zeros(self.cells)
        self.mean = 10000
        self.std = 10000

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
        self.ser.write(b"s")

    def update_plot_data(self):
        self.ser.write(b"s")
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
        temp[temp<0] = 0
        image = pg.ImageItem(temp)
        self.graphWidget.plotItem.clear()
        self.graphWidget.plotItem.addItem(image)
        # self.graphWidget.setImage(self.buffer, autoLevels=False, autoRange=False, autoHistogramRange=False, levels=(0, 1000))
        


# start the Qt App
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