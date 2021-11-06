import sys
import threading
import tkinter as tk

import tkinter as tk

import grpc
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib;

import protofiles_pb2_grpc, protofiles_pb2

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

Z=[]

def rungrpc():

    print('yeah')
    #global Z
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

    parts = stub.compute(request)
    for x in parts:
        print('Data found ! Received from the server ')
        a = x
        yield a.z


class App:
    def __init__(self):
        root = tk.Tk()
        root.title("Our GRPC")
        # canvas1 = tk.Canvas(root, width = 400, height = 300)

        # canvas1.pack()

        label_time = tk.Label(root, text='time')
        label_x = tk.Label(root, text='x0')
        label_y = tk.Label(root, text='y0')
        label_z = tk.Label(root, text='z0')
        label_dt = tk.Label(root, text='step')

        time1 = tk.Entry(root, width=8)
        time2 = tk.Entry(root, width=8)
        x0 = tk.Entry(root, width=16)
        y0 = tk.Entry(root, width=16)
        z0 = tk.Entry(root, width=16)
        dt = tk.Entry(root, width=16)

        # canvas1.create_window(20, 120, window=label_time)
        # canvas1.create_window(80, 120, window=time1)
        # canvas1.create_window(140, 120, window=time2)
        # canvas1.create_window(20, 160, window=label_x)
        # canvas1.create_window(100, 160, window=x0)
        # canvas1.create_window(20, 200, window=label_y)
        # canvas1.create_window(100, 200, window=y0)
        # canvas1.create_window(20, 240, window=label_z)
        # canvas1.create_window(100, 240, window=z0)
        # canvas1.create_window(20, 280, window=label_dt)
        # canvas1.create_window(100, 280, window=dt)
        # button1 = tk.Button(text='Start', width=16)
        # canvas1.create_window(100, 320, window=button1)
        # canvas1.create_rectangle(200, 100, 700, 500, fill="RED")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.x = np.linspace(-6, 6, 120)
        self.y = np.linspace(-6, 6, 120)
        self.X, self.Y = np.meshgrid(self.x, self.y)



        self.Z = np.cos(self.X)*np.sin(self.Y)
       # self.Z = np.sin(self.X) * np.cos(self.Y)
        self.line = self.ax.plot_surface(self.X[:60], self.Y[:60], self.Z[:60], rstride=1, cstride=1,
                                         cmap='winter', edgecolor='none')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        # self.canvas.get_tk_widget().create_rectangle(200, 100, 700, 500, fill="BLUE")
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ani = None

        grpcThread = threading.Thread(target=rungrpc)
        grpcThread.start()

        myThread = threading.Thread(target=self.animation)
        myThread.start()



        root.mainloop()


    def animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.data, fargs=(self.Z, self.line), interval=200, blit=False)

    def data(self, i, z, line):
        # z = np.sin(x+y+i)
        print('Checking for new data from the server :) ')
        # time.sleep(4)
        self.Z = np.cos(self.X) * np.sin(self.Y)
        self.ax.clear()
        self.line = self.ax.plot_surface(self.X, self.Y, self.Z, color='b')
        return self.line,



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
"""


# Launch ...
if __name__ == '__main__':
    rungrpc()

   # app = App()
   # app.exec_()