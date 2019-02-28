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

userID = '00010000000001'
now = datetime.datetime.now()
fileName = userID + '_' + str(now)[:10] + '.csv'
# writing data to a csv file to record the history of orders
print(fileName)
with open(fileName, mode = 'w', newline='') as order_history:
    myFields = ['order_ID', 'status', 'direction', 'time_in_force', 'timestamp',
                'stock_price', 'stock_quantity', 'trader_cash', 'current_stock']
    writer = csv.writer(order_history)
    writer.writerow(myFields)
    writer.writerows([[userID, 'unconfirmed', 'B', 99999, 384398343, 3333, 222, 1500, 120], 
                    [userID, 'confirmed', 'B', 99999, 384398343, 3333, 222, 1500, 120]])
    writer.writerow([userID, 'confirmed', 'B', 99999, 384398343, 3333, 222, 1500, 120])
    order_history.close()

def getLastOrderID(fileName):
    with open(fileName, 'r') as order_history:
        for row in reversed(list(csv.reader(order_history))):
            lastLine = row
            break
    print(lastLine)
    fullOrderID = str(lastLine[0])
    orderNumberStr = fullOrderID[4:]
    order_history.close()
    return int(orderNumberStr)

getLastOrderID(fileName)