from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol, Factory
from twisted.internet import reactor, protocol
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import binascii
import struct
from OUCH_parrot.simple_OUCH import *


# -----------------------
# TraderServer class: handles the traders connecting to the broker
# -----------------------
class TraderServer(Protocol):

    # keep track of all traders
    def connectionMade(self):
        self.factory.traders.append(self)
        traderID = self.factory.traders.index(self)
        print('Client ' + str(traderID) + ' connected.')

    # handles the orders received from traders
    def dataReceived(self, order):
        traderID = self.factory.traders.index(self)
        orderID = self.factory.orderID
        self.factory.orderID += 1
        print("Order #" + str(orderID) + " sent.")

        # decode order from bytes
        decodedOrder = order.decode().split(':')[1]
        orderType = decodedOrder[0]
        decodedOrder = decodedOrder[1:]
        quantity = decodedOrder.split('x')[0]
        decodedOrder = decodedOrder.split('x')[1]
        stock = decodedOrder.split('@')[0]
        price = decodedOrder.split('@')[1]

        decodedOrder = OuchClientMessages.EnterOrder(
            order_token='{:014d}'.format(randrange(1,100)).encode('ascii'), 
            buy_sell_indicator=orderType.encode(),
            shares=int(quantity),
            stock=stock.encode(),
            price=int(price),
            time_in_force=randrange(0,99999),
            firm=b'OUCH',
            display=b'N',
            capacity=b'O',
            intermarket_sweep_eligibility=b'N',
            minimum_quantity=1,
            cross_type=b'N',
            customer_type=b' ')

        # forward orders to exchange
        exchangeClientFactory = ClientFactory()
        def exchangeProtocol():
            return ExchangeClient(decodedOrder)
        exchangeClientFactory.protocol = exchangeProtocol
        reactor.connectTCP("localhost", 9001, exchangeClientFactory)

# -----------------------
# ExchangeClient class: handles the connection to the exchange server
# -----------------------
class ExchangeClient(Protocol):

    def __init__(self, traderOrder):
        self.traderOrder = traderOrder

    # forward orders to exchange server
    def connectionMade(self):
        self.transport.write(bytes(self.traderOrder))

    # handles exchange responses to orders
    def dataReceived(self, data):
        #parse_OUCH(binascii.a2b_hex(raw_response))

       
        #d = data.decode()
        #print("Exchange Server: ", d)
        
        #response = parse_OUCH(data)

        #msg_type = chr(data[0])
        #temp = chr(data[1])

        print(data)




    # for debugging, connection to exchange should not close
    def connectionLost(self, reason):
        print("ERROR: EXCHANGE CONNECTION LOST - ", reason)


# -----------------------
# Main: Set up trader server to wait for connections
# -----------------------
def main():
    traderServerFactory = ServerFactory()
    traderServerFactory.protocol = TraderServer
    traderServerFactory.traders = []
    traderServerFactory.orderID = 0
    reactor.listenTCP(8000, traderServerFactory)
    reactor.run()

if __name__ == '__main__':
    main()
