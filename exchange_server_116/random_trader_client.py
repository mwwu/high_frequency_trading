from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import time
from message_handler import decodeServerOUCH, decodeClientOUCH
import random
import numpy
from inventory import Inventory

# -----------------------
# RandomTraderClient class: sends orders to the broker
# -----------------------
class RandomTraderClient(Protocol):
    def __init__(self, inventory):
        self.inventory = inventory

    def connectionMade(self):
        reactor.callLater(0, self.sendRandomOrder)
        reactor.callLater(4, self.sendRandomOrder)
        reactor.callLater(8, self.sendRandomOrder)
        reactor.callLater(12, self.sendRandomOrder)

    def sendRandomOrder(self):
        # TODO: check this matches paper equations?

        # range 0.0 to 1.0
        randomNum = random.random() 

        prob_buy = 0.5
        buy_sell_indicator = 'S'
        if (randomNum < prob_buy):
            buy_sell_indicator = 'B'

        shares_rate_avg = 150
        shares = numpy.random.poisson(shares_rate_avg)

        mean_price = 200
        sd = 2
        price = round(numpy.random.normal(mean_price,sd))

        order = OuchClientMessages.EnterOrder(
            order_token='{:014d}'.format(0).encode('ascii'),
            buy_sell_indicator=buy_sell_indicator.encode(),
            shares=shares,
            stock=b'AMAZGOOG',
            price=price,
            time_in_force=randrange(0,99999),
            firm=b'OUCH',
            display=b'N',
            capacity=b'O',
            intermarket_sweep_eligibility=b'N',
            minimum_quantity=1,
            cross_type=b'N',
            customer_type=b' ')
        self.transport.write(bytes(order))
        print("Sent order: ", order)

    def dataReceived(self, data):
        ch = chr(data[0]).encode('ascii')
        if (ch == b'#'):
            print("BB/BO: ", data)
        else:
            msg_type, msg = decodeServerOUCH(data)
            if msg_type == b'A':
                self.inventory.confirmedOrder(
                    msg['order_token'], 
                    msg['buy_sell_indicator'], 
                    msg['shares'], 
                    msg['price']
                )

            elif msg_type == b'E':
                print('executed order')
                self.inventory.executedOrder(
                    msg['order_token'], 
                    msg['executed_shares']
                )
            self.inventory.printCurrentPositionDetailed()

# -----------------------
# Main function
# -----------------------
def main():
    inventory = Inventory(100, 1)
    def protocol():
        return RandomTraderClient(inventory)

    factory = ClientFactory()
    factory.protocol = protocol
    reactor.connectTCP("localhost", 8000, factory)
    reactor.run()

if __name__ == '__main__':
    main()
