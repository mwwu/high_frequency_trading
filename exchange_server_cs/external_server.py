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
from external_feeds import UnderlyingValue, BBBO

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
        self.buyStartTime = []
        self.buyEndTime = []
        self.buyPriceAxis = []

        self.sellStartTime = []
        self.sellEndTime = []
        self.sellPriceAxis = []

    def data_recieved_from_client(self, data):
        msg_type, msg = decodeClientOUCH(data)
        if msg_type == b'O':
            price = msg['price']
            time_in_force = msg['time_in_force']

            if msg['buy_sell_indicator'] == b'B':
                self.buyStartTime.append(self.time())
                self.buyEndTime.append(self.time() + time_in_force)
                self.buyPriceAxis.append(price/100)

            elif msg['buy_sell_indicator'] == b'S':
                self.sellStartTime.append(self.time())
                self.sellEndTime.append(self.time() + time_in_force)
                self.sellPriceAxis.append(price/100)

    def plotResults(self):
        plt.hlines(self.buyPriceAxis, self.buyStartTime, self.buyEndTime, color ="red", linewidth=0.5)
        plt.hlines(self.sellPriceAxis, self.sellStartTime, self.sellEndTime, color ="blue", linewidth=0.5)

"""
======================================

Twisted: This is where connections to the clients are connected

======================================
"""

class Client(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)

    # forward any data received to broker
    def dataReceived(self, data):
        self.factory.broker.data_recieved_from_client(data)

class ClientsFactory(ServerFactory):
    protocol = Client

    def __init__(self):
        self.clients = []
        self.initialTime = time.time()

        self.broker = Broker(self.time, self.clients)
        self.underlyingValueFeed = UnderlyingValue(self.time, self.clients)

    def stopFactory(self):
        with open('data_points.csv', mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(["ORDERS FOR BUYERS"])
            data_writer.writerow(self.broker.buyPriceAxis)
            data_writer.writerow(["ORDERS FOR SELLERS"])
            data_writer.writerow(self.broker.sellPriceAxis)
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
    # connect to clients
    reactor.listenTCP(8000, ClientsFactory())

    # schedule the end of the experiment
    reactor.callLater(30, reactor.stop)

    # start the event loop
    reactor.run()


if __name__ == '__main__':
    main()
