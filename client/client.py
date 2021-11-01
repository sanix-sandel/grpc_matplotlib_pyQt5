import sys

import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import numpy as np
import matplotlib.pyplot as plt

import grpc
import protofiles_pb2
import protofiles_pb2_grpc


class Dialog(QDialog):
    #NumGridRows = 3
    #NumButtons = 4

    def __init__(self):
        self.x = QLineEdit()
        self.y = QLineEdit()
        super(Dialog, self).__init__()
        self.createFormGroupBox()

        #buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ##buttonBox.accepted.connect(self.accept)
        #buttonBox.rejected.connect(self.reject)

        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)

        # addding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()



        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)



        self.setWindowTitle("Complete the form")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Complete the form")
        layout = QFormLayout()
        layout.addRow(QLabel("X:"), self.x)
        layout.addRow(QLabel("Y:"), self.y)

        self.formGroupBox.setLayout(layout)

    def getInfo(self):
        # printing the form information
        print("X", self.x.text())
        print("Y", self.y.text())

        # closing the window
        self.close()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        fig = plt.figure()
        self.ax = plt.axes(projection="3d")
        self.plotit()
        super(MplCanvas, self).__init__(fig)

    def plotit(self):
        self.x = np.linspace(-6, 6, 180)
        self.y = np.linspace(-6, 6, 180)#=>request(x=self.x, y=self.y)

        self.X, self.Y = np.meshgrid(self.x, self.y)#be removed

        self.Z = [] # from the server
       # print(" Z :", [x for x in self.Z.z], "\n")
        for x in self.run():
            i=[i for i in x.z]
            self.Z.extend([i])
        #print("Z received : ", self.Z)

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
        return stub.compute(request).z


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas(self)
        form=Dialog()


        self.setWindowTitle("my first window")



        #toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(form)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()