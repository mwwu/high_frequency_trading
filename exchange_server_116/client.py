
from __future__ import print_function

from twisted.internet import task
from twisted.internet.protocol import ClientFactory
from twisted.python import log
from twisted.internet.defer import Deferred

from sys import stdout
from maker_robot import Maker
from random_trader_client import RandomTraderClient
from inventory import Inventory
from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol


class Client(protocol.Protocol):
  def __init__(self, client_id):
    self.algorithms = "None"
    self.inventory = Inventory(0) 
    self.id = client_id
    self.order_tokens = {}  # key = order token and value = 'B' or 'S'
    self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
    self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
    self.bid_quantity = {}
    self.ask_quantity = {}
    self.best_bid = 0
    self.best_offer = 0
    self.bid_i = 0
    self.ask_i = 0

#=======Algorithm methods==========================
  def run_algorithm(self, algorithm):
      while algorithm != "None":
          if self.algorithm == "Maker":
              maker_instance = Maker()
          elif self.algorithm == "Random":
              random_instance = RandomTraderClient()

  def set_algorithm(self, algorithm):
    self.algorithm = algorithm

  def get_algorithm(self):
    return self.algorithm

  def get_id(self):
    return self.id

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
      self.transport.write("client %s has connected\n", self.id)

  def dataReceived(self, data):
      print("Received data:",data)
      self.transport.loseConnection()

#Look at megan's test_broker
#which is the connection object that i can grab? is it from buildProtocol?
#=====ClientFactory=========================

class ClientFactory(protocol.ClientFactory):

    protocol = Client

    def clientConnectionFailed(self, connector, reason):
        print ('connection failed:', reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print ('connection lost:', reason.getErrorMessage())


reactor.connectTCP('localhost', 8000, ClientFactory())
reactor.run()


