from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import struct
import numpy as np
import random as rand
import math

class EpsilonTrader():

  def __init__(self, client, V = 100, lmbda=50, mean=0, std=0.2):
    self.client = client

    self.V = V
    self.lmbda = lmbda
    self.mean = mean
    self.std = std

    waitingTime, priceDelta, buyOrSell = self.generateNextOrder()
    reactor.callLater(waitingTime, self.sendOrder, priceDelta, buyOrSell)

  def set_underlying_value(self, V): 
    self.V = V 

  def generateNextOrder(self):
    waitingTime = -(1/self.lmbda)*math.log(rand.random()/self.lmbda)
    priceEpsilon = np.random.normal(self.mean, self.std)
    randomSeed = rand.random()
    if (randomSeed > .5):
      buyOrSell = b'B'
    else:
      buyOrSell = b'S'
    return waitingTime, priceDelta, buyOrSell

  def sendOrder(self, priceDelta, buyOrSell):
    if(buyOrSell == b'S'):
      price = self.V + priceDelta
    if(buyOrSell == b'B'):
      price = self.V - priceDelta

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

