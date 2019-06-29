from twisted.internet import reactor, protocol
from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages
import collections
import socket
from random import randrange

class ClientServer(protocol.Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print('INSIDE CONNECTION_MADE OF BROKER: client connected')

    #00000000000000:B44xAMAZGOOG@33
    #00000000001000:B10xAMAZGOOG@1000
    def dataReceived(self, data):
        print("\nDATA RECEIVED FROM CLIENT: ", data)
        traderID = self.factory.clients.index(self)

        print('received from client', traderID, ': ' + data.decode())
        self.factory.book.append(data)

        # dictionaries used to calculate BB and BO
        buyStock = {} # key is price, value is quantity
        sellStock = {} # key is price, value is quantity

        #1. parse the message into our database TODO:  this has to work with replace orders
        text1 = data.decode()
        token = text1.split(':')
        print("Printing out token:\n")
        for t in token: print(t)
        print("\nFinished printing out token.")
        if (token[2][0] == 'B'):
          temp = token[2].split('B')
        else:
          temp = token[2].split('S')
        print("Printing out temp:\n")
        for t in temp: print(t)
        print("\nFinished printing out temp.")
        qShares = temp[1].split('x')
        stockName = qShares[1].split('@')

        # appending to dictionaries
        if (token[2][0] == 'B'):
            buyStock[stockName[1]] = qShares[0]
        else:
            sellStock[stockName[1]] = qShares[0]

        #2. send OUCH message to exchange server
        request = OuchClientMessages.EnterOrder(
            order_token='{:014d}'.format(traderID).encode('ascii'), #change to orderID after you figure that out
            buy_sell_indicator=token[1][0].encode(),
            shares=int(qShares[0]),
            stock=stockName[0].encode(),
            price=int(stockName[1]),
            time_in_force=randrange(0,99999),
            firm=b'OUCH',
            display=b'N',
            capacity=b'O',
            intermarket_sweep_eligibility=b'N',
            minimum_quantity=1,
            cross_type=b'N',
            customer_type=b' ')

        self.factory.exchangeServer.sendall(bytes(request))

        print('sent to exchange: ' + data.decode())

        #3. calculate best bid and best offer
        i = 0
        for key in sorted(buyStock):
            i += 1
            if (i == len(buyStock)):
                bestBid = (key, buyStock[key])
            bestBid = (key, buyStock[key])
            #print("bestBid\n", bestBid)
            break
            #print ("%s: %s" % (key, buyStock[key]))
        for key in sorted(sellStock):
            bestOffer = (key, sellStock[key])
            #print("bestOffer\n", bestBid.key)
            #print("bestOffer\n", bestBid.sellStock[key])
            break

        #4. broadcast BB BO to all the clients
        for c in self.factory.clients:
            request = "BB2x3BO5x6"
            c.transport.write(bytes(request.encode()))
        print('sent to all clients: ' + request)

def main():
    factory = protocol.ServerFactory()
    factory.protocol = ClientServer
    factory.clients = []
    factory.book = [] # book used to keep track of all orders received from clients

    s = socket.socket()
    s.connect(('localhost', 9001))
    factory.exchangeServer = s

    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
