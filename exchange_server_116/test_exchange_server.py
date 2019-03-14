from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor

class ExchangeServer(Protocol):
    def connectionMade(self):
        self.transport.write(b"Hi, I am the exchange")

    def dataReceived(self, data):
        print("Broker: ", data)

def main():
    exchangeServerFactory = ServerFactory()
    exchangeServerFactory.protocol = ExchangeServer
    reactor.listenTCP(8001, exchangeServerFactory)
    reactor.run()

if __name__ == '__main__':
    main()
