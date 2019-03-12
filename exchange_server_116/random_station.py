# Goal: to first be able to read client's input and run it to Exchange
#       second to get output from exchange server and save it
#       third keep track of client's shares and cash

# Tasks:
#   1. Parsing functions for input
#   2. Set up wallet structure
#   3. Receive and parse output
#      Communication with another file for output (exchange.py line 116)
#      goes into wallet, communicate wallet with client, then client goes to exchange
#   4. Update wallet for buying and selling
#   5. Cash limitation for purchases
#   6. Add or withdraw cash

#   2&6 FM, 3&4 WMW, 1&5 JMC

import sys
import asyncio
import asyncio.streams
import configargparse
import logging as log
import re
# import binascii
from random import randrange
import itertools
import datetime
import random
import numpy
import csv
from multiprocessing import Process, Pool

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages


class Trade_Station:
    def __init__(self, cash, id):
        self.id = id
        self.cash = cash
        self.inventory = {}
        self.order_tokens = {}  # key = order token and value = 'B' or 'S'
        self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
        self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
        self.bid_quantity = {}
        self.ask_quantity = {}

    def summary(self):  # should remove order_tokens when transaction is complete
        print("id:{} cash:{}\n"
              " inventory:{} \n"
              "order_token:{}\n"
              " bid_stocks{}\n"
              " ask_stocks{}\n"
              .format(self.id,
                      self.cash,
                      self.inventory,
                      self.order_tokens,
                      self.bid_stocks,
                      self.ask_stocks))


    def buy_share(self, share, price,amt):
        if share not in self.inventory:
            self.inventory[share] = amt
        else:
            self.inventory[share] += amt
        self.cash -= amt * price

    def sell_share(self, share, price, amt):
        if share not in self.inventory:
            self.inventory[share] = 0
        self.inventory[share] -= amt
        self.cash += amt * price

    def get_id(self):
        return self.id

    def get_cash(self):
        return self.cash

    def get_inventory(self):
        return self.inventory

class CSVManager:
    def __init__(self, userID):
        now = datetime.datetime.now()
        self.fileName = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '-' + str(now.minute) + '_' + '{:04d}'.format(userID) + '.csv'
        try:
            # Check if a given .csv file exists.
            file = open(self.fileName, 'r')
            file.close()
        except IOError:
            with open(self.fileName, 'w') as history:
                myFields = ['order_ID', 'status', 'direction', 'time_in_force', 'timestamp',
                            'stock_price', 'stock_quantity', 'trader_cash', 'current_stock']
                writer = csv.DictWriter(history, fieldnames=myFields)
                writer.writeheader()
                history.close()
                    
    def logLine(self, orderID, status, direction, time_in_force, timestamp, stock_price, stock_quantity, trader_cash, current_stock):
        newRow = {'order_ID': orderID,
                    'status': status,
                    'direction': direction,
                    'time_in_force': time_in_force,
                    'timestamp': timestamp,
                    'stock_price': stock_price,
                    'stock_quantity': stock_quantity,
                    'trader_cash': trader_cash,
                    'current_stock': current_stock}
        try:
            with open(self.fileName, 'a', newline='') as history:
                writer = csv.DictWriter(history, newRow.keys())
                writer.writerow(newRow)
                history.close()
        except IOError:
            print("Writer error")

p = configargparse.ArgParser()
p.add('--port', default=9001)
p.add('--host', default='127.0.0.1', help="Address of server")
options, args = p.parse_known_args()

def trade(id):
    user = Trade_Station(0, id)
    log.basicConfig(level=log.DEBUG)
    log.debug(options)
    csvManager = CSVManager(user.get_id())

    async def client():
        reader, writer = await asyncio.streams.open_connection(
            options.host,
            options.port,
            loop=loop)

        async def send(request):
            writer.write(bytes(request))
            await writer.drain()

        async def recv():
            try:
                header = (await reader.readexactly(1))
            except asyncio.IncompleteReadError:
                log.error('connection terminated without response')
                return None
            message_type = OuchServerMessages.lookup_by_header_bytes(header)
            try:
                payload = (await reader.readexactly(message_type.payload_size))
            except asyncio.IncompleteReadError as err:
                log.error('Connection terminated mid-packet!')
                return None

            response_msg = message_type.from_bytes(payload, header=False)
            return response_msg

        # Builds the order message according to parameters passed.
        async def build_message():
            indicator = random.random()
            prob_buy = 0.5
            buy_sell_builder = 'S'
            if (indicator < prob_buy):
                buy_sell_builder = 'B'
            shares_rate_avg = 150
            shares_builder = numpy.random.poisson(shares_rate_avg)
            mean_price = 200
            sd = 2
            price_builder = round(numpy.random.normal(mean_price,sd))
            time_in_force_builder = 99999
            return [buy_sell_builder, shares_builder, price_builder, time_in_force_builder]

        # Logs the message to the .csv file.
        async def update(output, client, msg_type):
            # We don't need to log the failed attempts of user trading with itself:
            if msg_type == 'Q':
                return
            # Order confirmed
            # e.g. A: 80139293594000:00010000000010(63):B144xAMAZGOOG@203:16
            elif msg_type == 'A':
                timestamp = int(output.split(":")[1])
                parsed_token = output[17:31]
                purchase_details = output.split(":")[3] # e.g. B144xAMAZGOOG@203
                buy_sell = list(purchase_details)[0]
                quantity = "".join((list(purchase_details.split("x")[0]))[1:])
                price = purchase_details.split("@")[1]
                share_name = (purchase_details.split("x")[1]).split("@")[0]
            # Order executed
            # e.g. E: 80139293594000:00010000000010m14:18@201:6
            elif msg_type == 'E':
                timestamp = int(output.split(":", 2)[1])
                parsed_token = output[17:31]
                print(parsed_token)
                price_and_shares = output.split(":", 3)[3]
                quantity = int(price_and_shares.split("@", 1)[0])
                price = int(price_and_shares.split("@", 1)[1])
                buy_sell = user.order_tokens[parsed_token]
                if parsed_token in user.order_tokens and buy_sell == 'B':
                    share_name = [user.bid_stocks[i] for i in user.bid_stocks if i == parsed_token][0]
                    user.buy_share(share_name, price, quantity)

                elif parsed_token in user.order_tokens and buy_sell == 'S':
                    share_name = [user.ask_stocks[i] for i in user.ask_stocks if i == parsed_token][0]
                    user.sell_share(share_name, price, quantity)
            to_log = [parsed_token, msg_type, buy_sell, 'X', timestamp, price, quantity, user.cash, user.inventory[share_name]]
            print(to_log)
            csvManager.logLine(parsed_token, msg_type, buy_sell, 'X', timestamp, price, quantity, user.cash, user.inventory[share_name])

        while True:
            message_type = OuchClientMessages.EnterOrder
            for index in itertools.count():
                user_input = await build_message()  #why does this not return a list?
                # print(user_input)
                # ['B', 200, 12, 2432, 'Ouch']
                binary_buysell = user_input[0].encode("ascii")
                buy_sell = user_input[0]
                userTokenPart = '{:04d}'.format(user.get_id())
                orderTokenPart = '{:010d}'.format(index)
                token = '' + userTokenPart + orderTokenPart
                btoken = token.encode('ascii')
                stock = 'AMAZGOOG'
                bstock = stock.encode('ascii')
                price = user_input[2]
                num_shares = user_input[1]
                time_in_force = user_input[3]
                firm = b'OUCH'

                user.order_tokens[token] = buy_sell
                if (buy_sell == 'B'):
                    user.bid_stocks[token] = stock
                else:
                    user.ask_stocks[token] = stock

                request = message_type(
                     order_token=btoken,
                     buy_sell_indicator=binary_buysell,
                     shares=num_shares,
                     stock=bstock,
                     price=price,
                     time_in_force=time_in_force,
                     firm=b'OUCH',
                     display=b'N',
                     capacity=b'O',
                     intermarket_sweep_eligibility=b'N',
                     minimum_quantity=1,
                     cross_type=b'N',
                     customer_type=b' ')

                if stock not in user.inventory:
                    user.inventory[stock] = 0
                log.info("Sending Ouch message: %s", request)
                await send(request)
                timestamp = int(datetime.datetime.now().timestamp())
                to_log = [token, 'O', buy_sell, 'X', timestamp, price, num_shares, user.cash, user.inventory[stock]]
                print(to_log)
                csvManager.logLine(token, 'O', buy_sell, time_in_force, timestamp, price, num_shares, user.cash, user.inventory[stock])

                response = await recv()
                log.info("Received response Ouch message: %s:%d", response, len(response))

                while True:
                    try:
                        response = await asyncio.wait_for(recv(), timeout=0.5)
                        log.info("Received response Ouch message: %s:%d", response, len(response))
                        output = str(response)
                        await update(output, user, output[0])
                    except asyncio.TimeoutError:
                        break
                await asyncio.sleep(4.0)

        writer.close()
        asyncio.sleep(4.0)

    loop = asyncio.get_event_loop()
# creates a client and connects to our server
    try:
        loop.run_until_complete(client())
    finally:
        loop.close()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for id in range(0, int(sys.argv[1])):
        p = Process(target = trade, args=(id,))
        p.start()