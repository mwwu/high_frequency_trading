from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
from twisted.internet import reactor
from random import randrange
from message_handler import decodeServerOUCH, decodeClientOUCH


# -----------------------
# Broker class: manages all of the servers!
# note: only work with one stock right now
# -----------------------
class Broker():

    bytes_needed = {
        'S': 10,
        'E': 40,
        'C': 28,
        'U': 80,
        'A': 66,
        'Q':33,
    }
    def __init__(self):
        self.traders = []
        self.orderID = 0
        self.exchange = None


        #TODO: add more logic, ie remove when order is executed
        # orders[order_token] = traderID
        self.orders = {}

        # bids = [(price, order_token), ...], lowest first
        self.bids = []

        # offers = [(price, order_token), ...], highest first
        self.offers = []

        self.order_imbalance = 0

    # sends response from exchange back to intended trader
    def sendToTrader(self, data):
        # print("The data in sendToTrader is:{}".format(data))
        header = chr(data[0])

        # look for the number of bytes needed based on the header
        try:
            bytes_needed = self.bytes_needed[header]
        except KeyError:
            raise ValueError('unknown header %s.' %header)

        # if there are extra bytes in the buffer then make data start at the next message
        if len(data) >= bytes_needed:
            remainder = bytes_needed
            more_data = data[remainder:]
            data = data[:bytes_needed]

        msg_type, msg = decodeServerOUCH(data)

        # order Accepted, add to broker's books
        if msg_type == b'A':
            bid_offer = (msg['price'], msg['order_token'], msg['shares'])
            if msg['buy_sell_indicator'] == b'B':
                self.bids.append(bid_offer)
                self.bids = sorted(self.bids)
            elif msg['buy_sell_indicator'] == b'S':
                self.offers.append(bid_offer)
                self.offers = sorted(self.offers, reverse=True)
            traderID= self.orders[msg['order_token']]
            self.traders[traderID].transport.write(data)

        # order Executed, remove from broker's books
        elif msg_type == b'E':
            print('executed: ', msg)

            # TODO: implement executed!!!!!!
            order_token = msg['order_token']
            traderID= self.orders[order_token]
            self.traders[traderID].transport.write(data)

        #call function again cause there is remaining data in the buffer
        if len(more_data):
            self.sendToTrader(more_data)
        else:
            self.broadcastBBBO(data)





    # TODO: What to do if there are NO best bids / best off???
    def broadcastBBBO(self, data):
        # print("The data in broadcastBBBO is:{}".format(data))
        header = chr(data[0])
        msg_type, msg = decodeServerOUCH(data)
        if msg_type == b'A':
            print('BIDS: ', self.bids)
            print('OFFS: ', self.offers)
            for t in self.traders:
                bb = 0
                if len(self.bids) > 0:
                    bb, x, y = self.bids[0]
                bo = 0
                if len(self.offers) > 0:
                    bo, x, y = self.offers[0]
                msg = "#BB" + str(bb) + ":BO" + str(bo)
                print("msg:{}\n".format(msg))
                t.transport.write(bytes(msg.encode()))

        #TODO calculate order imbalance here


# -----------------------
# TraderServer class: handles the traders connecting to the broker
# -----------------------
class TraderServer(Protocol):

    bytes_needed = {
        'S': 10,
        'E': 40,
        'C': 28,
        'U': 80,
        'A': 66,
        'Q': 33,
        'O': 49
    }


    def __init__(self, broker):
        self.broker = broker

    # keep track of all traders
    def connectionMade(self):
        self.broker.traders.append(self)
        traderID = self.broker.traders.index(self)
        print('Client ' + str(traderID) + ' connected.')

    # orders from traders a blindly forwarded to exchange
    def dataReceived(self, data):
        traderID = self.broker.traders.index(self)
        orderID = self.broker.orderID
        header = chr(data[0])
        more_data = None
        try:
            bytes_needed = self.bytes_needed[header]
        except KeyError:
            raise ValueError('unknown header %s.' %header)

        if len(data) >= bytes_needed:
            remainder = bytes_needed
            more_data = data[remainder:]
            data = data[:bytes_needed]

        order_token = self.broker.exchange.sendOrder(orderID, data)
        self.broker.orders[order_token] = traderID

        print("Order #" + str(orderID) + " sent.")
        self.broker.orderID += 1

        if len(more_data):
            self.dataReceived(more_data)


# -----------------------
# ExchangeClient class: handles the connection to the exchange server
# -----------------------
class ExchangeClient(Protocol):

    def __init__(self, broker):
        self.broker = broker

    def connectionMade(self):
        self.broker.exchange = self


    # handles responses from exchange
    def dataReceived(self, data):
        reactor.callLater(0, self.broker.sendToTrader, data=data)
        #not the best way to do this but i made sendToTrader call broadcastBBO after sendtotrader is done
        # reactor.callLater(1, self.broker.broadcastBBBO, data=data)

    def sendOrder(self, orderID, order):
        print("ORDER:{}\n".format(order))
        if len(order):
            msg_type, msg = decodeClientOUCH(order)
            order_token = '{:014d}'.format(orderID).encode('ascii')
            if msg_type == b'O':
                msg['order_token'] = order_token
            self.transport.write(bytes(msg))
            return order_token

# -----------------------
# How everything is connected! :D
# TraderClient -(port: 8000)-> TraderServer | Broker | ExchangeClient -(port:9001)->ExchangeServer
# -----------------------
def main():
    broker = Broker()

    # set up connection to the exchange server
    exchangeClientFactory = ClientFactory()
    def exchangeClient():
        return ExchangeClient(broker)
    exchangeClientFactory.protocol = exchangeClient
    reactor.connectTCP("localhost", 9001, exchangeClientFactory)

    # set up server for trader connections
    traderServerFactory = ServerFactory()
    def traderServer():
        return TraderServer(broker)
    traderServerFactory.protocol = traderServer
    reactor.listenTCP(8000, traderServerFactory)
    reactor.run()


if __name__ == '__main__':
    main()
