from bluepy import btle
import numpy as np
import pyqtgraph as pg
from collections import deque
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time
import serial 
import PIL


        
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        # self.data_line =  self.graphWidget.plot(self.delegate.times, self.delegate.vals, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.ser = serial.Serial('/dev/ttyUSB0', 250000)
        self.calibration = []
    def update_plot_data(self):
        # read new charac value
        # self.delegate.handleNotification(0,0)
        # self.data_line.setData(())  # Update the data.
        # print(self.ser.readline())
        data = self.ser.readline()
        #  split on "/"
        data = data.split(b"/")
        # print(len(data))
        #  split on ","
        data = [x.split(b",") for x in data]

        # 
        if len(data) < 3:
            return
        data = data[1]
        # print(len(data))
        #  convert to int from byte
        for i in range(len(data)):
            data[i] = float(int.from_bytes(data[i], byteorder='little'))
            # data[i] = int(data[i])
        #  convert to numpy array
        # print(data[:3])s
        matrix = np.array(data[:252], dtype=np.float32)
        if len(self.calibration) < 200:
            matrix = np.max(matrix) - matrix
            # matrix = matrix / np.max(matrix)
            self.calibration.append(matrix)
            # self.calibration.pop(0)
        else:
            # print(matrix.shape)
            calib = np.array(self.calibration)
            # # print("ss",np.mean(calib, axis=0).shape)
            # matrix = matrix - np.mean(calib, axis=0) + 20 s
            # do a soft max 

            # matrix = np.exp(matrix) / np.sum(np.exp(matrix))s
            matrix = np.max(matrix) - matrix
            # matrix = matrix / np.max(matrix)
            mean = np.mean(calib, axis=0)
            std = np.std(calib, axis=0)
            matrix = (matrix - mean) / std
            matrix = np.abs(matrix)
            matrix[matrix<3.5] = 0
            # matrix = np.exp(matrix) / np.sum(np.exp(matrix))

            # matrix = np.max(matrix) - matrix
            # matrix = matrix / np.max(matrix)
            # matrix = matrix - np.mean(calib, axis=0)
            # matrix = matrix / 10
            # matrix[matrix<0.01] = 0
            print(matrix)
            # print(matrix)

        # reshape patrix 12*21
        matrix = matrix.reshape((12,21), order='F')

        image = pg.ImageItem(matrix)
        #  plot matrix 
        self.graphWidget.clear()
        self.graphWidget.plotItem.addItem(image)
        #  write the values in th epixels

        #             self.graphWidget.plotItem.addItem(pg.TextItem(text=str(round(matrix[i,j],3)), color=(0,0,0), anchor=(j,i), border='w', fill=(255,255,255,100)))

        
        
    
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')

    exit(0)

# start the Qt App
app = QtWidgets.QApplication([])
w = MainWindow()
w.show()
app.exec_()
# dev.disconnect()s
while True:
    # if dev.waitForNotifications(1.0):
        # handleNotification() was called
        # continue
    # print("Waiting...")
    pass