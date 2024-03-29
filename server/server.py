import sys

from concurrent import futures
import logging
import grpc
import time

import protofiles_pb2
import protofiles_pb2_grpc

import numpy as np
from math import *

class ComputeFunctionServicer(protofiles_pb2_grpc.ComputeFunctionServicer):

    def __init__(self):
        pass

    def z_function(self, X, Y):
        return np.sin(X) * np.sin(Y)

    def compute(self, request, context):
        self.X, self.Y = np.meshgrid(np.array(request.x), np.array(request.y))
        z = self.z_function(self.X, self.Y)
        z = z.tolist()
        Z=protofiles_pb2.DataResponse()

        for zarr in z:
            zr=protofiles_pb2.array()
            zr.z.extend(zarr)
            Z.z.extend([zr])
        #print("Type of ", type(Z))
        return Z
        #print("Z : ", Z)

#        for array in Z:
#            arr=protofiles_pb2.array()
#            arr.z.extend(array)

#        array1=protofiles_pb2.array()
#        array1.z.extend(z1)


#        Z=protofiles_pb2.DataResponse()

#        print("array1 ", array1)
#        Z.z.extend([array1])
#        print("Z :", Z)
#        print(Z)
#        return Z



# Create a server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

protofiles_pb2_grpc.add_ComputeFunctionServicer_to_server(ComputeFunctionServicer(), server)

print('Starting server. Listening on port 5000')

server.add_insecure_port('[::]:5000')
server.start()

try:
    while True:
        time.sleep(86400)
except:
    server.stop(0)
