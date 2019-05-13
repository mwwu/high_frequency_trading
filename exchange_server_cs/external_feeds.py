from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory, ClientFactory
import random as rand
import numpy as np
import math
import matplotlib.pyplot as plt
from struct import *
from message_handler import decodeServerOUCH, decodeClientOUCH
import time
import csv

"""
===== Underlying Value Feed =====

This is the underlying V, that will control where the traders tend
to submit orders. When the state of the underlying value changes,
all traders will be notified.

Note: All underlying value broadcasts will start with: @

==================================
"""
class UnderlyingValue():
    def __init__(self, time, clients, V=100, lmbda=1, mean=0, std=.5):
        # keep track of subscribers
        self.time = time
        self.clients = clients

        # initialize constants for random number generators
        #self.T = 0
        self.V = V
        self.lmbda = lmbda
        self.mean = mean
        self.std = std

        # initialize graph for data visualization
        self.timeAxis = []
        self.valueAxis = []

        self.broadcast()

        # schedule the first price jump (uses poisson process)
        waitingTime, jumpHeight = self.generateNextJump()
        reactor.callLater(waitingTime, self.jump, waitingTime, jumpHeight)

    # controls the waiting time and the height of the next jump
    def jump(self, waitingTime, jumpHeight):
        self.V += jumpHeight
        self.broadcast()

        # store values for data visualization
        self.timeAxis.append(self.time())
        self.valueAxis.append(self.V)

        waitingTime, jumpHeight = self.generateNextJump()
        reactor.callLater(waitingTime, self.jump, waitingTime, jumpHeight)

    # send message out to all clients
    def broadcast(self):
        msg = "@" + str(self.V)
        for client in self.clients:
            m = pack('cf', b'@', self.V)
            client.transport.write(bytes(m))

    # implements the poisson process and normal distribution
    def generateNextJump(self):
        waitingTime = -(1/self.lmbda)*math.log(rand.random()/self.lmbda)
        jumpHeight = np.random.normal(self.mean, self.std)
        return (waitingTime, jumpHeight)

    # called after the factory ends
    def plotResults(self):
        plt.hlines(self.valueAxis, self.timeAxis[:-1], self.timeAxis[1:], linewidth=3.3)


"""
========== BBBO Feed ==========

This is the current state of BBBO. When the state of the BBBO changes
(everytime an order is executed, all traders will be notified.

================================
"""
class BBBO():
    def __init__(self):
        print("to be defined")
