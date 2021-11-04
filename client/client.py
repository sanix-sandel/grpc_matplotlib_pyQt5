import sys
import threading
import time

import matplotlib
import matplotlib.axes
from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib import animation
from matplotlib.animation import TimedAnimation
import matplotlib; matplotlib.use("TkAgg")


matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import numpy as np
import matplotlib.pyplot as plt

import grpc
import protofiles_pb2
import protofiles_pb2_grpc

"""
def run():
    channel = grpc.insecure_channel("localhost:5000")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        sys.exit('Error connecting to server')

    stub = protofiles_pb2_grpc.ComputeFunctionStub(channel)
    x = np.linspace(-6, 6, 5)
    y = np.linspace(-6, 6, 5)

    request = protofiles_pb2.DataRequest()
    request.x.extend(x.tolist())
    request.y.extend(y.tolist())

    parts=stub.compute(request)
    for x in parts:

        print('Data Received from server ', x)
        a=x
        print(dir(a))
        #a=next(parts)
        #print(a.z[0])
       

myDataLoop = threading.Thread(name='myDataLoo', target=run, daemon=True,
                                      args=())
myDataLoop.start()

myDataLoop.join()
"""



class Communicate(QObject):
    data_signal = pyqtSignal(float)


class MplCanvas(FigureCanvasQTAgg):

    def update(self):
        # z = np.sin(x+y+i)
        print('called')
       # time.sleep(2)
        self.z = np.cos(self.X) * np.sin(self.Y)
        self.ax.clear()
        self.line = self.ax.plot_surface(self.X, self.Y, self.z, color='b')
        return self.line,

    def __init__(self):

        # n = 2.*np.pi
        self.fig = plt.figure()
        #self.ax = fig.add_subplot(111, projection='3d')
        self.ax=plt.axes(projection="3d")
        super(MplCanvas, self).__init__(self.fig)
        self.x = np.linspace(-6, 6, 120)
        self.y = np.linspace(-6, 6, 120)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.Z = np.sin(self.X) * np.cos(self.Y)
        self.line = self.ax.plot_surface(self.X[:60], self.Y[:60], self.Z[:60], color='b')

        self.ani = animation.FuncAnimation(self.fig, self.update, fargs=(self.Z, self.line), interval=10, blit=False)
        plt.ion
        #dataThread=threading.Thread(name='mydata', target=self.update, daemon=True)
        #dataThread.start()

        #plt.show()


    #def run(self):
        #mySrc = Communicate()
        #mySrc.data_signal.connect(callBack)
     #   channel = grpc.insecure_channel("localhost:5000")
    #    try:
     #       grpc.channel_ready_future(channel).result(timeout=10)
     #   except grpc.FutureTimeoutError:
      #      sys.exit('Error connecting to server')
      #  stub = protofiles_pb2_grpc.ComputeFunctionStub(channel)

    #    request = protofiles_pb2.DataRequest()
    #    request.x.extend(self.x.tolist())
    #    request.y.extend(self.y.tolist())
    #    self.a=stub.compute(request)
        #for part in self.a:
        #    self.Z=[]
        #    for x in part.z:
        #        i=[i for i in x.z]
        #        self.Z.extend([i])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas()
        self.setWindowTitle("my first window")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(sc)
        #sc.plotit()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()