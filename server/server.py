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

        return np.tan(X) * np.sin(Y)

    def compute(self, request, context):
        print('server called')

        self.X, self.Y = np.meshgrid(np.array(request.x), np.array(request.y))
        z = self.z_function(self.X, self.Y)
        z = z.tolist()
        i=1
        while i<4:
            Z = protofiles_pb2.DataResponse()
            for zarr in z:
                zr=protofiles_pb2.array()
                zr.z.extend(zarr)
                Z.z.extend([zr])
            print(i, ' Data sent to the client !')
            yield Z
            i+=1
            time.sleep(4)





# Create a server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

protofiles_pb2_grpc.add_ComputeFunctionServicer_to_server(ComputeFunctionServicer(), server)

print('Starting server. Listening on port 5000 - Streaming ')

server.add_insecure_port('[::]:5000')
server.start()

try:
    while True:
        time.sleep(86400)
except:
    server.stop(0)
