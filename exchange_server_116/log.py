import sys
import asyncio
import asyncio.streams
import configargparse
from random import randrange
import time
import numpy
# writing to csv file
import csv
import datetime


userID = '0001'
now = datetime.datetime.now()
fileName = userID + '_' + str(now)[:10] + '.csv'
# writing data to a csv file to record the history of orders
print(fileName)
with open(fileName, mode = 'w') as order_history:
    myFields = ['trader_ID', 'status', 'direction', 'time_in_force', 'timestamp',
                'stock_price', 'stock_quantity', 'trader_cash', 'current_stock']
    writer = csv.DictWriter(order_history, fieldnames=myFields)
    writer.writeheader()
    order_history.close()
