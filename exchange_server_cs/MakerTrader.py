from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import struct
import numpy as np
import random as rand
import math


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

class MakerTrader():

  def __init__(self, client, V = 100, lmbda=50, mean=0, std=0.2):
    self.client = client

    self.V = V
    self.lmbda = lmbda
    self.mean = mean
    self.std = std


    self.bid_quantity = {}
    self.ask_quantity = {}
    self.best_bid = 0 
    self.best_offer = 0 
    self.bid_i = 0 
    self.ask_i = 0

    waitingTime, priceDelta, buyOrSell = self.generateNextOrder()
    reactor.callLater(waitingTime, self.sendOrder, priceDelta, buyOrSell)

  def set_underlying_value(self, V): 
    self.V = V 

  def new_ask(self):
    # print("\n MAKER_ROBOT: inside new_ask()\n")
    ask_price = self.best_bid - S_CONST * aggressiveness
    self.ask_i = ask_price
    return ask_price

  def new_bid(self):
    # print("\n MAKER_ROBOT: inside new_bid()\n")
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

  def generateNextOrder(self):
    waitingTime = 0
    priceDelta = 0
    randomSeed = rand.random()
    if (randomSeed > .5):
      buyOrSell = b'B'
      priceDelta = self.new_bid()
      #waitingTime = self.latent_bid()
    else:
      buyOrSell = b'S'
      priceDelta = self.new_ask()
      #waitingTime = self.latent_offer()

    return waitingTime, priceDelta, buyOrSell

  def sendOrder(self, priceDelta, buyOrSell):
    price = self.V + priceDelta

    order = OuchClientMessages.EnterOrder(
      order_token='{:014d}'.format(0).encode('ascii'),
      buy_sell_indicator=buyOrSell,
      shares=1,
      stock=b'AMAZGOOG',
      price=int(price * 10000),
      time_in_force=4,
      firm=b'OUCH',
      display=b'N',
      capacity=b'O',
      intermarket_sweep_eligibility=b'N',
      minimum_quantity=1,
      cross_type=b'N',
      customer_type=b' ')
    self.client.transport.write(bytes(order))

    waitingTime, priceDelta, buyOrSell = self.generateNextOrder()
    reactor.callLater(waitingTime, self.sendOrder, priceDelta, buyOrSell)

