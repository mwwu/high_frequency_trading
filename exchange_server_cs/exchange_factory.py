from twisted.internet.protocol import Protocol, ClientFactory

class Exchange(Protocol):
    def connectionMade(self):
        self.factory.broker.exchange = self

    def dataReceived(self, data):
        print(data)
        
class ExchangeFactory(ClientFactory):
    protocol = Exchange

    def __init__(self, broker):
        self.broker = broker

