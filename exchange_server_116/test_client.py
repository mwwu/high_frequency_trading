"""
Client for simple Ouch Server
"""

import sys
import asyncio
import asyncio.streams
import configargparse
import logging as log
# import binascii
from random import randrange
import itertools

from exchange_server_116.inventory import Inventory
from exchange_server_116.state import OrderType


from exchange_server_116.OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

def main():
    inventory = Inventory(100, 1)
    inventory.printCurrentPositionDetailed()
    inventory.unconfirmedOrder(
        "AMAZGOOG",
        OrderType.BUY,
        2.5,
        2,
        "ABC111")
    inventory.unconfirmedOrder(
        "AMAZGOOG",
        OrderType.SELL,
        20,
        5,
        "ABC112")
    inventory.printCurrentPositionDetailed()
    inventory.confirmedOrder("ABC112")
    inventory.printCurrentPositionDetailed()
    inventory.executedOrder("ABC112")
    inventory.printCurrentPositionDetailed()

if __name__ == '__main__':
    main()
