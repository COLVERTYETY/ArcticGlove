import numpy as np
import pyqtgraph as pg
from collections import deque
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time
import serial 


        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.setValue(0)
        self.slider1.setTickInterval(1)
        self.slider1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider2.setMinimum(3)
        self.slider2.setMaximum(1000)
        self.slider2.setValue(10)
        self.slider2.setTickInterval(50)
        self.slider2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        # self.setCentralWidget(self.graphWidget)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.graphWidget)
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # widget for slider
        self.graphWidget.setBackground('w')
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
        matrix = matrix.reshape((12,21), order='F')
        # rot 90
        matrix = np.rot90(matrix, 3)
        m_copy = matrix.copy()
        if len(self.calibration) < 500:
            # matrix = matrix / np.max(matrix)
            self.calibration.append(matrix)
            # self.calibration.pop(0)
    
        # print(matrix.shape)
        q = self.slider2.value()
        threshold = self.slider1.value()/10
        calib = np.array(self.calibration[:q])
        mean = np.mean(calib, axis=0)
        std = np.std(calib, axis=0)
        # matrix = (matrix - mean) / std
        # matrix = np.abs(matrix)
        # matrix = matrix / np.max(matrix)
        matrix = matrix - mean
        m_copy = m_copy - mean + 100
        matrix = np.abs(matrix)
        matrix/= std
        # get slider value
        # print(slider_value)
        matrix[matrix < threshold] = 0.0
        print(q,len(self.calibration), threshold, np.max(matrix), np.min(matrix), np.mean(matrix), np.std(matrix))

        # matrix = np.concatenate((matrix, m_copy), axis=1)
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