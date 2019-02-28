import sys
import asyncio
import asyncio.streams
import configargparse
from random import randrange
import time
import numpy
# writing to csv file
import csv

def main():
    userID = '0001'
    user = Trade_Station(1000000, userID)
    now = datetime.datetime.now()
    fileName = userID + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.csv'
    # writing data to a csv file to record the history of orders
    history = open(fileName, 'w')
    with history:
        myFields = ['trader_ID', 'status', 'direction', 'time_in_force', 'timestamp',
                    'stock_price', 'stock_quantity', 'trader_cash', 'current_stock']
        writer = csv.DictWriter(fileName, fieldnames=myFields)
        writer.writeheader()
