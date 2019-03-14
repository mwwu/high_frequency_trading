from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor

#connects to the broker
class TraderClient(Protocol):
	def connectionMade(self):
		self.transport.write(b"Hi, I am a trader")

	def dataReceived(self, data):
		print("Broker: ", data)


def main():
    traderClientFactory = ClientFactory()
    traderClientFactory.protocol = TraderClient
    reactor.connectTCP("localhost", 8000, traderClientFactory)
    reactor.run()


if __name__ == '__main__':
    main()
