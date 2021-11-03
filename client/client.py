import sys
import time

import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import numpy as np
import matplotlib.pyplot as plt

import grpc
import protofiles_pb2
import protofiles_pb2_grpc

""""
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
    for x in range(0, 3):
        print('Data Received from server ', x)
        a=next(parts)
        print(a.z[0])
       

run()
"""



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):

        fig = plt.figure()
        self.ax = plt.axes(projection="3d")

        super(MplCanvas, self).__init__(fig)

        self.x = np.linspace(-6, 6, 120)
        self.y = np.linspace(-6, 6, 120)
        self.run()
    def plotit(self):

        self.x = np.linspace(-6, 6, 120)
        self.y = np.linspace(-6, 6, 120)#=>request(x=self.x, y=self.y)

        self.X, self.Y = np.meshgrid(self.x, self.y)#be removed

        self.Z = [] # from th    server
        #for x in next(self.run()):
        #    i=[i for i in x.z]
        #    self.Z.extend([i])

        #self.ax.plot_surface(self.X, self.Y, np.array(self.Z), rstride=1, cstride=1,
         #                    cmap='winter', edgecolor='none')
        #self.ax.set_title('surface')

    def run(self):
        print('run ')
        channel = grpc.insecure_channel("localhost:5000")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        stub = protofiles_pb2_grpc.ComputeFunctionStub(channel)

        request = protofiles_pb2.DataRequest()
        request.x.extend(self.x.tolist())
        request.y.extend(self.y.tolist())

        parts = stub.compute(request)
        for i in parts:
            a = next(parts)
            print(' Z received')
            #yield a.z


if __name__=='__main__':
    sc = MplCanvas()
    sc.run()





""""




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas(self)
        self.setWindowTitle("my first window")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(sc)
        sc.plotit()
        #sc.run()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
       # self.show()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
    
"""""