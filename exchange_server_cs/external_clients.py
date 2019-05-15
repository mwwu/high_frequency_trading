from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import struct
import numpy as np
import random as rand
import math
import RandomTrader

class ExternalClient(Protocol):
	def __init__(self):
		self.trader = RandomTrader.RandomTrader(self)

	def connectionMade(self):
		print("client connected")

	def dataReceived(self, data):
		# forward data to the trader, so they can handle it in different ways
		ch = chr(data[0]).encode('ascii')
		if (ch == b'@'):
			c, V = struct.unpack('cf', data)
			self.trader.set_underlying_value(V)
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
