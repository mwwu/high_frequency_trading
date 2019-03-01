from twisted.internet import reactor, protocol
import socket
from exchange_server_116.OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

class Echo(protocol.Protocol):

    def connectionMade(self):
        self.factory.clients.append(self)

    def dataReceived(self, data):
        self.factory.book.append(data)
        print('received: '+data.decode())
        #self.transport.write(data)
        for c in self.factory.clients:
            c.transport.write(data)

        # dictionaries
        buyStock = {}
        sellStock = {}

        #1. parse the message into our database
        text1 = data.decode()
        token = text1.split(':')
        if (token[1][0] == 'B'):
          temp = token[1].split('B')
        else:
          temp = token[1].split('S')
        shares = temp[1].split('x')
        stock = shares[1].split('@')

        print('Token = '+ token[0] + '\n'
              + 'Buy or Selling = '+ token[1][0] + ' | '
              + 'Quantity of Shares = '+ shares[0] + ' | '
              + 'Stock Name= '+ stock[0] + ' | '
              + 'Price = '+ stock[1])

        #2. send OUCH message to exchange server
        request = OuchClientMessages.EnterOrder(
            order_token='{:014d}'.format(0).encode('ascii'),
            buy_sell_indicator=b'B',
            shares=22,
            stock=b'AMAZGOOG',
            price=33,
            time_in_force=44,
            firm=b'OUCH',
            display=b'N',
            capacity=b'O',
            intermarket_sweep_eligibility=b'N',
            minimum_quantity=1,
            cross_type=b'N',
            customer_type=b' ')
        #self.factory.exchangeServer.sendall(bytes(request))
        self.factory.exchangeServer.sendmsg(data.decode())

        #3. calculate best bid and best offer

        #4. broadcast BB BO to all the clients
        for c in self.factory.clients:
            # first is best bid, second is best offer
            request = "2x3:5x6;"
            c.transport.write(bytes(request.encode()))

def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    factory.clients = []
    factory.book = []
    s = socket.socket()
    s.connect(('localhost', 9001))
    factory.exchangeServer = s
    reactor.listenTCP(8000,factory)
    # will not exit run
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
