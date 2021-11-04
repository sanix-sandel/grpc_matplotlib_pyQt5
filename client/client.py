import sys
import threading
import time

import matplotlib
from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.animation import TimedAnimation

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







class Communicate(QObject):
    data_signal = pyqtSignal(float)





class MplCanvas(FigureCanvasQTAgg, TimedAnimation):

    def __init__(self, parent=None):
        fig = plt.figure()
        self.ax = plt.axes(projection="3d")
        super(MplCanvas, self).__init__(fig)
        self.x = np.linspace(-6, 6, 120)
        self.y = np.linspace(-6, 6, 120)
        self.Z = []
        myDataLoop = threading.Thread(name='myDataLoop', target=self.receiveData, daemon=True,
                                      args=())
        myDataLoop.start()
        TimedAnimation.__init__(self, fig, interval=50, blit=True)


    def new_frame_seq(self):
        return iter(range(self.x.size))

    def plotit(self):
        time.sleep(4)
        self.X, self.Y = np.meshgrid(self.x, self.y)#be removed
        #self.Z=np.cos(self.X)*np.sin(self.Y)
        self.ax.plot_surface(self.X, self.Y, np.array(self.Z), rstride=1, cstride=1,
                             cmap='winter', edgecolor='none')
        self.ax.set_title('surface')


    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            #self.abc += 1
            #print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def receiveData(self):
        print('rece')
        self.run()

    #def addData_callbackFunc(self):
    #    for x in next(run()):
    #        i = [i for i in x.z]
    #        self.Z.extend([i])
    #    return

    def run(self):
        channel = grpc.insecure_channel("localhost:5000")
        #mySrc = Communicate()
        #mySrc.data_signal.connect(addData_callbackFunc)
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        stub = protofiles_pb2_grpc.ComputeFunctionStub(channel)

        request = protofiles_pb2.DataRequest()
        request.x.extend(self.x.tolist())
        request.y.extend(self.y.tolist())
        a=stub.compute(request)
        print(dir(a))
        self.Z=[]
        for x in next(a).z:
            i=[i for i in x.z]
            self.Z.extend([i])
        #print(self.Z)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas(self)
        self.setWindowTitle("my first window")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(sc)
        sc.plotit()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
