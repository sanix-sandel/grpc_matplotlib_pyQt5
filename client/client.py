import sys

import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import numpy as np
import matplotlib.pyplot as plt

import grpc
import protofiles_pb2
import protofiles_pb2_grpc

"""
def run():
    channel = grpc.insecure_channel("localhost:5000")
    stub = protofiles_pb2_grpc.ComputeFunctionStub(channel)

   # x=protofiles_pb2.x(elt=x)
    #y=protofiles_pb2.y(elt=y)

    request=protofiles_pb2.DataRequest()
    print(request)
    request.x.extend([1.01, 2.34, 2.02])
    request.y.extend([8.4, 2.1, 8.9])
    #print(request)
    print(stub.compute(request))


if __name__=='__main__':
    run()
"""


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        # fig = Figure(figsize=(width, height), dpi=dpi)



        fig = plt.figure()
        self.ax = plt.axes(projection="3d")
        self.plotit()
        super(MplCanvas, self).__init__(fig)

    #def z_function(self, x, y):  # to the server
    #    return np.cos(x) * np.sin(y)  # np.sin(np.sqrt(x ** 2 + y ** 2))

    def plotit(self):
        self.x = np.linspace(-6, 6, 30)
        self.y = np.linspace(-6, 6, 30)#=>request(x=self.x, y=self.y)

        self.X, self.Y = np.meshgrid(self.x, self.y)#be removed

        self.Z = [] # from the server
       # print(" Z :", [x for x in self.Z.z], "\n")
        for x in self.run().z:

            print("type x: ",type(x))

            #print([i for i in x.z])
            i=[i for i in x.z]
            self.Z.extend([i])
        print("Z : ", self.Z)

        self.ax = plt.axes(projection='3d')
        self.ax.plot_surface(self.X, self.Y, np.array(self.Z), rstride=1, cstride=1,
                             cmap='winter', edgecolor='none')
        self.ax.set_title('surface');
        # plt.show()

    def run(self):
        channel=grpc.insecure_channel("localhost:5000")
        stub=protofiles_pb2_grpc.ComputeFunctionStub(channel)

        request=protofiles_pb2.DataRequest()
        request.x.extend(self.x.tolist())
        request.y.extend(self.y.tolist())
        return stub.compute(request)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self)
        # sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.setWindowTitle("my first window")

        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()