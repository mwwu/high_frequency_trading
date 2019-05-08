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
===== Underlying Value Class =====

This is the underlying V, that will control where the traders tend 
to submit orders. When the state of the underlying value changes, 
all traders will be notified.

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
            #client.transport.write(bytes(msg.encode()))

    # implements the poisson process and normal distribution
    def generateNextJump(self):
        waitingTime = -(1/self.lmbda)*math.log(rand.random()/self.lmbda)
        jumpHeight = np.random.normal(self.mean, self.std)
        return (waitingTime, jumpHeight)

    # called after the factory ends
    def plotResults(self):
        plt.hlines(self.valueAxis, self.timeAxis[:-1], self.timeAxis[1:])


"""
========== BBBO Class ==========

This is the current state of BBBO. When the state of the BBBO changes 
(everytime an order is executed, all traders will be notified.

================================
"""
class BBBO():
    def __init__(self):
        print("to be defined")


"""
========== Broker Class ==========

This is where incoming orders are handled
================================
"""

class Broker():
    def __init__(self, time, clients):
        self.time = time
        self.clients = clients

        # initialize for data visualization of orders
        self.timeAxis = []
        self.priceAxis = []

    def orderReceived(self, data):
        price = unpack('f', data)
        self.timeAxis.append(self.time())
        self.priceAxis.append(price)

    def plotResults(self):
        plt.scatter(self.timeAxis, self.priceAxis, .5)

"""
===== TWISTED Factory & Protocol =====

This is where the server and connections are handled.

======================================
"""

class ExternalServer(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)

    # forward any data received to broker
    def dataReceived(self, data):
        self.factory.broker.orderReceived(data)

class ExternalServerFactory(ServerFactory):
    protocol = ExternalServer

    def __init__(self):
        self.clients = []
        self.initialTime = time.time()

        self.broker = Broker(self.time, self.clients)
        self.underlyingValueFeed = UnderlyingValue(self.time, self.clients)

    def stopFactory(self):
        with open('data_points.csv', mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(["ORDERS"])
            data_writer.writerow(self.broker.priceAxis)
            data_writer.writerow(["UNDERLYING VALUES"])
            data_writer.writerow(self.underlyingValueFeed.valueAxis)

        data_file.close()
        print("Finished writing to data_points.csv!\n")
        self.broker.plotResults()
        self.underlyingValueFeed.plotResults()
        plt.show()


    def time(self):
        return time.time() - self.initialTime

def main():
    reactor.listenTCP(8000, ExternalServerFactory())

    # schedule the end of the experiment
    reactor.callLater(10, reactor.stop)

    # start the event loop
    reactor.run()


if __name__ == '__main__':
    main()