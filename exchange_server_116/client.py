
from __future__ import print_function

from twisted.internet import task
from twisted.internet.protocol import ClientFactory
from twisted.python import log
from twisted.internet.defer import Deferred

from sys import stdout
# import make_connection
from twisted.internet.protocol import Protocol
from twisted.internet import protocol

from twisted.words.protocols import irc

from make_connection import Greeter
from make_connection import gotProtocol
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

#import make_connection
from make_connection import Greeter
from make_connection import gotProtocol

from twisted.protocols.basic import LineReceiver

from inventory import Inventory

aggressiveness = 0.5
b_x = 0.5 #slider 
b_y = 0.5 #slider 

a_x = 0.5 #slider 
a_y = 0.5 #slider 

x = 1 #get from broker 
y = 1 #get from broker


S_CONST = 1

class Client(LineReceiver):
  def __init__(self):
    self.algorithms = "None"
    self.inventory = Inventory(0) 
    self.id = 0
    self.order_tokens = {}  # key = order token and value = 'B' or 'S'
    self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
    self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
    self.bid_quantity = {}
    self.ask_quantity = {}
    self.best_bid = 0
    self.best_offer = 0
    self.bid_i = 0
    self.ask_i = 0
    self.point = TCP4ClientEndpoint(reactor, "localhost", 8000)
  
  def run_algorithm(self, algorithm):
    while(algorithm != "None"):
      if(self.algorithm == "Maker"):
        
  def set_algorithm(self, algorithm):
    self.algorithm = algorithm

  def get_algorithm(self):
    return self.algorithm

  def get_id(self):
    return self.inventory.id

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

  def connectionMade(self):
    msg =str(self.build_Message())
    
    print("Message sent to broker printing..:\n")
    print(msg)
    print("Finished printing message to broker.\n")
    self.transport.write(bytes((msg).encode()))

  def connectionMade_2(self):
    msg = str(self.build_Message_2('B'))
    self.transport.write(bytes((msg).encode()))

  def lineReceived(self, line):
    print("received from server:", line)

  def dataReceived(self, data):
    print("data received from server:", data.decode())
    #BB2x3BO5x6
    self.best_bid = 3
    self.best_offer = 4
    self.connectionMade_2()

class TraderFactory(ClientFactory):
    protocol = Client

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

def main(reactor):
    factory = TraderFactory()
    reactor.connectTCP('localhost', 8000, factory)
    return factory.done

if __name__ == '__main__':
    task.react(main)
