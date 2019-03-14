from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol, Factory
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString, HostnameEndpoint

#handles exchange connection
class ExchangeClient(Protocol):
    def connectionMade(self):
        self.transport.write(b"Hi exchange, I am the broker")
        print("1:", self)

    def dataReceived(self, data):
        print("Exchange Server: ", data)

    def send(self, exchangeClient, data):
        print("should be sending...")

    def sendMessage(self):
        self.transport.write("Hi server, I finally work")

#handles incoming traders
class TraderServer(Protocol):
    exchange = None

    def __init__(self, exchange):
        self.exchange = exchange

    def connectionMade(self):
        self.transport.write(b"Hi trader, I am the broker")

    def dataReceived(self, data):
        print("Client: ", data)
        self.exchange.sendMessage()


class TraderServerFactory(ServerFactory):
    exchange = None

    def __init__(self, exchange):
        self.exchange = exchange

    def buildProtocol(self, addr):
        return TraderServer(self.exchange)

def main():
    #setting up to connect to exchange server
    """
    exchangeClientFactory = ClientFactory()
    exchangeClientFactory.protocol = ExchangeClient
    reactor.connectTCP("localhost", 8001, exchangeClientFactory)
    """

    exchangeEndpoint = HostnameEndpoint(reactor, 'localhost', 8001)
    exchangeFactory = Factory.forProtocol(ExchangeClient)
    exchange = ClientService(exchangeEndpoint, exchangeFactory)
    exchange.sendAll(b"lskdjflsdkjf")
    #setting up for traders to connect
    reactor.listenTCP(8000, TraderServerFactory(exchange))
    reactor.run()


if __name__ == '__main__':
    main()
