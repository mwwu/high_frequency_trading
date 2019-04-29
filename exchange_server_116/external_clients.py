from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import struct
import numpy as np
import random as rand
import math

class RandomTrader():
	def __init__(self, client, V = 100, lmbda=100, mean=0, std=.4):
		self.client = client

		self.V = V 
		self.lmbda = lmbda
		self.mean = mean
		self.std = std

		waitingTime, priceDelta = self.generateNextOrder()
		reactor.callLater(waitingTime, self.sendOrder, priceDelta)

	def underlyingValueFeed(self, V):
		self.V = V

	def generateNextOrder(self):
	    waitingTime = -(1/self.lmbda)*math.log(rand.random()/self.lmbda)
	    priceDelta = np.random.normal(self.mean, self.std)
	    return waitingTime, priceDelta

	def sendOrder(self, priceDelta):
		price = self.V + priceDelta

		self.client.transport.write(bytes(struct.pack('f', price)))

		waitingTime, priceDelta = self.generateNextOrder()
		reactor.callLater(waitingTime, self.sendOrder, priceDelta)


class ExternalClient(Protocol):
	def __init__(self):
		self.trader = RandomTrader(self)

	def connectionMade(self):
		print("client connected")

	def dataReceived(self, data):
		# forward data to the trader, so they can handle it in different ways
		ch = chr(data[0]).encode('ascii')
		if (ch == b'@'):
			c, V = struct.unpack('cf', data)
			self.trader.underlyingValueFeed(V)
		else:
			print("unhandled message type")

# -----------------------
# Main function
# -----------------------
def main():
    externalClientFactory = ClientFactory()
    externalClientFactory.protocol = ExternalClient
    reactor.connectTCP("localhost", 8000, externalClientFactory)
    reactor.run()

if __name__ == '__main__':
    main()
