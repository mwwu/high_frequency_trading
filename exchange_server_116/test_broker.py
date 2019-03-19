from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol, Factory
from twisted.internet import reactor, protocol

# -----------------------
# ExchangeClient class: handles the connection to the exchange server
# -----------------------

class ExchangeClient(Protocol):

    def __init__(self, traderOrder):
        self.traderOrder = traderOrder

    # forward orders from traders to the exchange server
    def connectionMade(self):
        self.transport.write(self.traderOrder)

    # handles exchange responses to orders
    def dataReceived(self, data):
        print("Exchange Server: ", data)


# -----------------------
# TraderServer class: handles the traders connecting to the broker
# -----------------------

class TraderServer(Protocol):

    # set up a trader that connects to the broker
    def connectionMade(self):
        print('client connected')

    # handles the orders received from traders
    def dataReceived(self, data):
        print("Client: ", data)

        exchangeClientFactory = ClientFactory()
        def exchangeProtocol():
            return ExchangeClient(data)
        exchangeClientFactory.protocol = exchangeProtocol
        reactor.connectTCP("localhost", 8001, exchangeClientFactory)


# -----------------------
# Main: Set up trader server to wait for connections
# -----------------------

def main():
    traderServerFactory = ServerFactory()
    traderServerFactory.protocol = TraderServer
    reactor.listenTCP(8000, traderServerFactory)
    reactor.run()

if __name__ == '__main__':
    main()
