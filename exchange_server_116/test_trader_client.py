from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange

# -----------------------
# TraderClient class: sends orders to the broker
# -----------------------
class TraderClient(Protocol):
	def connectionMade(self):
		self.transport.write(b'00000000000000:B44xAMAZGOOG@33')

	def dataReceived(self, data):
		print("Received from Broker: ", data)


# -----------------------
# Main function
# -----------------------
def main():
    traderClientFactory = ClientFactory()
    traderClientFactory.protocol = TraderClient
    reactor.connectTCP("localhost", 8000, traderClientFactory)
    reactor.run()

if __name__ == '__main__':
    main()
