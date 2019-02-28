import sys
import asyncio
import asyncio.streams
import configargparse
import logging as log
import re
# import binascii
from random import randrange
import itertools
import time
import random

from inventory import Inventory
from orderStatus import OrderType
from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

#TODO: still has to be built
from randomTrader import RandomTrader
from makerTrader import MakerTrader
from takerTrader import TakerTrader

# get client input on whether they want to sell or buy
# send the messages directly to the server
# server sends message to back to client

# how to handle updates
# how to handle time
# how to handle orders coming in -> queue?
# how to send messages to server
# how to parse information from server

class Broker:
    def getClientInput(client):
        #currently hardcoding the market participants
        time = 0
        robot1 = RandomTrader()
        robot2 = MakerTrader()
        robot3 = TakerTrader()

        # order = {} \\ key is order token, value is client
        #each loop represents 1 unit of time passing
        while true:
            time++

            order1 = robot1.run(time, BB, BO)

    def Clientinput(client):
        buySell = input("Do you want to buy or sell stock? Type B for sell and S for sell")
        if (buySell == B):
            price = input("What price do you want to buy it for?")
            quantity = input("How much stock do you want to buy?")
        if (buySell == S):
            quantity = input("How much stock do you want to sell?")
            price = input("How much do you want to sell it for?")
        return (buySell, price, quantity)

    def BestBidOffer():
        for i in orders

def main():
    robot1 = inventory_class(0, 1)
