
from __future__ import print_function
from twisted.internet.protocol import ClientFactory, Protocol
# from maker_robot import Maker
# from random_trader_client import RandomTraderClient
from inventory import Inventory
from twisted.internet import reactor, protocol
from message_handler import decodeServerOUCH, decodeClientOUCH


from collections import deque
import maker_robot 
#from maker_robot import Maker, main
#from maker_robot import *
import random


class Client(Protocol):
    bytes_needed = {
        'B': 10,
        'S': 10,
        'E': 40,
        'C': 28,
        'U': 80,
        'A': 66,
        'Q': 33,
    }
    def __init__(self, _algorithm = "None"):
        super()
        self.algorithm = _algorithm 
        self.inventory = Inventory(0)
        self.order_tokens = {}  # key = order token and value = 'B' or 'S'
        self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
        self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
        self.counter = 0


    def get_cash(self):
        return self.inventory.cash

    def get_inventory(self):
        return self.inventory.inventory

    def add_withdraw_cash(self):
        print("Do you want to add or withdraw cash? ")
        while (1):
            add_or_withdraw = input("Type A for add and W for withdraw. ")
            if (add_or_withdraw == 'A'):
                add = input("How much money do you want to add? ")
                self.inventory.cash += int(add)
                break;
            elif (add_or_withdraw == 'B'):
                sub = input("How much money do you want to withdraw? ")
                self.inventory.cash -= int(sub)
                break;
            else:
                print("Please try again.")


    def update_cash_inventory(self, output):
        parsed_token = output[18:32]

        price_and_shares = output.split(":", 3)[3]
        executed_shares = int(price_and_shares.split("@", 1)[0])
        executed_price = int(price_and_shares.split("@", 1)[1])

        print("output={}".format(output))
        cost = executed_price * executed_shares
        print("\nHere is the parsed token:{}\n".format(parsed_token))
        print("\nHere are the executed_shares {}\n".format(executed_shares))
        print("\nHere are the executed_price {}\n".format(executed_price))
        if parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'B':
            self.inventory.cash -= cost
            share_name = [self.bid_stocks[i] for i in self.bid_stocks if i == parsed_token]
            self.inventory.inventory[share_name[0]] = executed_shares

        elif parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'S':
            self.inventory.cash += cost
            share_name = [self.ask_stocks[i] for i in self.ask_stocks if i == parsed_token]

        if share_name[0] in self.inventory.inventory:
            self.inventory.inventory[share_name[0]] -= executed_shares
        if self.inventory.inventory[share_name[0]] == 0:
            del self.inventory.inventory[share_name[0]]


  
#======Twisted connection methods=================
    def connectionMade(self):
        print("connection made!")
        self.factory.maker.begin_maker()
        #now we just need to build and send a message to the broker!

    def dataReceived(self, data):
        header = chr(data[0]).encode('ascii')
        if (header == b'#'):
            print("BB/BO: ", data)
        else:
            try:
                msg_type, msg = decodeServerOUCH(data)
                print("SERVER SAYS: ", msg)
            except KeyError:
                 raise ValueError('unknown header %s.' % header)

        print("About to build another message in Maker")

        #creates 100 buy or sell orders randomly
        random_val = random.randint(0,2)
        if self.counter < 30:
            if random_val == 0:
                self.counter += 1
                self.factory.maker.build_Message(b'B')
            else:
                self.counter += 1
                self.factory.maker.build_Message(b'S')
        else:
            print("\nFinished!!!\n")


# =====ClientFactory=========================

class ClientConnectionFactory(ClientFactory):

    protocol = Client
    def __init__(self):
        super()
        self.connection = None
        self.maker = maker_robot.Maker(self)

    def buildProtocol(self, addr):
        self.connection = ClientFactory.buildProtocol(self, addr)
        print("connection in client is:",self.connection)
        return self.connection

    def clientConnectionFailed(self, connector, reason):
        print ('connection failed:', reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print ('connection lost:', reason.getErrorMessage())
        reactor.stop()

    def connectToBroker(self, addr):
        reactor.connectTCP('localhost',8000, self)
        reactor.run()


def main():

    factory = ClientConnectionFactory()
    reactor.connectTCP('localhost', 8000, factory)
    reactor.run()

if __name__ == '__main__':
    main()





