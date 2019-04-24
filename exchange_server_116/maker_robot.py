#~Bid_i(t) = BB_i - S * B(x(t), y(t))
#~Ask_i(t) = BO_i + S * A(x(t), y(t))


#Bid = min{[~Bid]s, BO - 2S}
#Ask = max{[~Ask]s, BB + 2S}



##
#create a robot  [X]

#connect to the proxy server []
# receive execute message and parse it [X]
# update robot's cash and inventory [X]
# Receive BA and BO []
# price = formulas above ^ [X]

# create messages []

# Send new message []
#

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

import client

aggressiveness = 0.5
b_x = 0.5 #slider 
b_y = 0.5 #slider 

a_x = 0.5 #slider 
a_y = 0.5 #slider 

x = 1 #get from broker 
y = 1 #get from broker


S_CONST = 1

MAX_ASK = 2147483647
MIN_BID = 0

#class Maker_Client(irc.IRCClient):
#class Maker_Client(Protocol):
class Maker(Protocol):
  def __init__(self, clientFactory):
    print("\n MAKER_ROBOT: inside __init__()\n")
    self.bid_quantity = {}
    self.ask_quantity = {}
    self.best_bid = 0 
    self.best_offer = 0 
    self.bid_i = 0 
    self.ask_i = 0
    self.clientFactory = clientFactory
    self.connection = self.clientFactory.connection


  def new_ask(self):
    print("\n MAKER_ROBOT: inside new_ask()\n")
    ask_price = self.best_bid - S_CONST * aggressiveness
    self.ask_i = ask_price
    return ask_price

  def new_bid(self):
    print("\n MAKER_ROBOT: inside new_bid()\n")
    bid_price = self.best_offer - S_CONST * aggressiveness
    self.bid_i = bid_price
    return bid_price

  def bid_aggressiveness(b_x, b_y, x, y):
    print("\n MAKER_ROBOT: inside bid_aggressiveness()\n")
    """
    B(x(t), y(t))
    x: order imbalance
    y: inventory position
    """
    return - b_x * x + b_y * y

  def sell_aggressiveness(a_x, a_y, x, y):
    print("\n MAKER_ROBOT: inside sell_aggressiveness()\n")
    """
    A(x(t), y(t))
    x: order imbalance
    y: inventory position
    """
    return a_x * x - a_y * y

  def latent_bid(bb, S, bid_aggressiveness):
    print("\n MAKER_ROBOT: inside latent_bid()\n")
    """
    LB(t)
    bb: best bid
    S: half a tick
    """
    return bb - S * bid_aggressiveness

  def latent_offer(bo, S, sell_aggressiveness):
    print("\n MAKER_ROBOT: inside latent_offer()\n")
    """
    LB(t)
    bb: best offer
    S: half a tick
    """
    return bo + S * sell_aggressiveness

  def dataReceived(self, data):
    print("\n MAKER_ROBOT: inside dataReceived()\n")
    print("data received from server:", data.decode())
    #BB2x3BO5x6
    self.best_bid = 3
    self.best_offer = 4

  def build_Message(self, Buy_or_Sell):
    print("\n MAKER_ROBOT: inside build_Message()\n")
    if(Buy_or_Sell == 'S'):
      Price = self.new_ask() 
    else:
      Price = self.new_bid()

    #parameters: buy/sell and price
    message_type = OuchClientMessages.EnterOrder
    request = message_type (
      order_token='{:014d}'.format(1000).encode('ascii'), 
      buy_sell_indicator=Buy_or_Sell, shares=10, 
      stock=b'AMAZGOOG', 
      price=Price, 
      time_in_force=10000, 
      firm=b'OUCH',
      display=b'N', 
      capacity=b'O', 
      intermarket_sweep_eligibility=b'N', 
      minimum_quantity=1, 
      cross_type=b'N', 
      customer_type=b' '
    )
    self.connection.transport.write(request)

  #great now we have the connection. we can use whatever methods are in Client protocol with connection
  #but broker still breaks when connected
  def begin_maker(self):
    print("\n MAKER_ROBOT: inside begin_maker()\n")
    print("connection in maker is :", self.connection)
    self.build_Message('B')


#great now we have the connection. we can use whatever methods are in Client protocol with connection
#but broker still breaks when connected
def main():
    print("\n MAKER_ROBOT: inside main()\n")
    factory = client.ClientConnectionFactory()
    conn = factory.connection
    print("connection:", conn)
    print("cash is {}".format( conn.get_cash()))
    # factory.maker.build_Message('B')
    # factory.connectToBroker(("localhost", 8000))



if __name__ == '__main__':
    main()

