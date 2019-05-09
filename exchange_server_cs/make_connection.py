from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol


class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("%s" % msg)

    # handle the BBO here and create new formula

    def dataReceived(self, data):
        print("in client's dataReceived")
        print(data)




def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)




#point = TCP4ClientEndpoint(reactor, "localhost", 8000)
#d = connectProtocol(point, Greeter())
#d.addCallback(gotProtocol)
#reactor.run()
