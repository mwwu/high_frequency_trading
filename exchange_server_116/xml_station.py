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
import numpy
# import ElementTree
import xml.etree.ElementTree as ET
# writing to csv file
import csv

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

# WRITING DATA TO AN XML FILE
# class XML_Structure:
#     def _init_(self, trader):
#         # add trader node as root
#         traderTree = ET.element('trader')
#         root = traderNode.getroot()
#         self.root = root
#         root.set('id', id)
#
#         # add wallet node: cash & inventory
#         walletNode = ET.SubElement(root, 'wallet')
#         cashNode = ET.SubElement(walletNode, 'cash')
#         inventoryNode = ET.SubElement(walletNode, 'inventory')
#         # add inventory attribute: stock
#         stockNode = ET.SubElement(inventoryNode, 'stock')
#         # add stock attributes: value & quantity
#         valueNode = ET.SubElement(stockNode, 'value')
#         quantityNode = ET.SubElement(stockNode, 'quantity')
#
#         # add history node: order
#         historyNode = ET.SubElement(root, 'history')
#         orderNode = ET.SubElement(historyNode, 'order')
#
#         # create an XML file with the results
#         myTrader = ET.tostring(traderTree)
#         self.fileName = str(trader.get_id()) + ".xml"
#         traderNode.write(fileName)
#
#     def getFileName(self):
#         return self.fileName
#
#     def getRoot(self):
#         return self.root
#
#     # function to edit cash in the file
#     def modify_cash(self, newCash):
#         traderNode = ET.parse(self.getFileName())
#         root = getRoot(self)
#         root[0][0].text = newCash
#
#
#     # function to edit stock in the file
#     def editStock(self, stockName, value, quantity):
#
#
#     # function to add new order to history - need to edit the "update()" function
#     def add_order(self):
#         # add order attributes: status, direction, price, quantity, time in force, timestamp


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
        # self.xml = XML_Structure(self)

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

    #--------BUY_SHARE AND SELL_SHARE FUNCTIONS NOT USED--------
    # def buy_share(self, share, price,
    #               amt):  # probably shouldnt use these functions because it is adding to inventory before
    #     if share not in self.inventory:  # it has crossed
    #         self.inventory[share] = amt
    #     else:
    #         self.inventory[share] += amt
    #     self.cash -= amt * price
    #
    # def sell_share(self, share, price, amt):
    #     if share not in self.inventory:
    #         print("You do not own these shares")
    #     else:
    #         self.inventory[share] -= amt
    #         self.cash += amt * price

    def get_id(self):
        return self.id

    def get_cash(self):
        return self.cash

    def get_inventory(self):
        return self.inventory

    # Task 6: Add and Withdraw Cash from Wallet
    def add_withdraw_cash(self):
        print("Do you want to add or withdraw cash? ")
        while (1):
            add_or_withdraw = input("Type A for add and W for withdraw. ")
            if (add_or_withdraw == 'A'):
                add = input("How much money do you want to add? ")
                self.cash += int(add)
                break;
            elif (add_or_withdraw == 'B'):
                sub = input("How much money do you want to withdraw? ")
                self.cash -= int(sub)
                break;
            else:
                print("Please try again.")


p = configargparse.ArgParser()
p.add('--port', default=9001)
p.add('--host', default='127.0.0.1', help="Address of server")
options, args = p.parse_known_args()

class CSVBase:
    def _init_(self, userID):
        self.fileName = userID + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.csv'

    def getFileName():
        return self.fileName

    def getLastOrderID():


    def getCash():


    def getStock():



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

    log.basicConfig(level=log.DEBUG)
    log.debug(options)

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

        # Tasks 1 and 5
        async def build_message():
            print("Type q to start again")
            buy_sell_builder = await verify_buy_sell()
            shares_builder = await verify_shares(buy_sell_builder)
            price_builder = await verify_price(buy_sell_builder, shares_builder)
            time_in_force_builder = await verify_time()
            firm_builder = await verify_firm(buy_sell_builder)
            return [buy_sell_builder, shares_builder, price_builder, time_in_force_builder, firm_builder]

        async def verify_buy_sell():
            print("Type B to buy or S to sell")
            buy_sell_input = input()
            if (buy_sell_input == 'q'):
                build_message()
            elif (buy_sell_input == 'B' or buy_sell_input == 'S'):
                return buy_sell_input
            else:
                print("Type B for buy, S for sell or q to start again:")
                verify_buy_sell()

        async def verify_shares(buy_sell_builder):
            print("Number of shares: more than 0, less than a million")
            shares_input = input()
            if (shares_input == 'q'):
                build_message()
            try:
                shares_int = int(shares_input)
            except ValueError:
                print("You need to provide an integer.")
                verify_shares(buy_sell_builder)
            if (shares_int < 0 or shares_int > 1000000):
                print("You provided a value outside of range.")
                verify_shares(buy_sell_builder)
            else:
                # if(buy_sell_builder == 'S'):
                # if (shares_int > seller.getShares()):
                #     print("You don't have enough shares in your wallet")
                #     verify_shares()
                return shares_int

        async def verify_price(buy_sell_builder, shares_builder):
            print("Provide the price at which you are happy to trade:")
            price_input = input()
            # Check if the price is an integer:
            try:
                price_int = int(price_input)
            except ValueError:
                print("You need to provide an integer.")
                verify_price(buy_sell_builder, shares_builder)
            # Check if price is in the range:
            if (price_int < 0 or price_int > (10 ** 9 - 100)):
                print("You provided a value outside of range.")
                verify_price(buy_sell_builder, shares_builder)
            else:
                return price_int

        async def verify_time():
            print("Provide the time in force; minimum 0, max 99999")
            time_in_force_input = input()
            # time_in_force=randrange(0,99999)
            try:
                time_int = int(time_in_force_input)
            except ValueError:
                print("You need to provide an integer.")
                verify_time()
            if (time_int < 0 or time_int > 99999):
                print("You provided the time outside of range.")
                verify_time()
            else:
                return time_int

        async def verify_firm(buy_sell_builder):
            print("What firm are you trading for:")
            firm_input = input()
            # if (buy_sell_builder == 'S'):
            #     if not firm_input.belongsTo(portfolio):
            #         print("You don't have this firm")
            return firm_input

        # Task 6: Add and Withdraw Cash from Wallet
        async def add_withdraw_cash(self):
            print("Do you want to add or withdraw cash? ")
            add_or_withdraw = input("Type A for add and W for withdraw. ")
            while (1):
                if (add_or_withdraw == 'A'):
                    add = input("How much money do you want to add? ")
                    self.cash += add
                    break;
                elif (add_or_withdraw == 'B'):
                    sub = input("How much money do you want to withdraw? ")
                    self.cash -= sub
                    break;
                else:
                    print("Please try again.")

        async def update(ex_msg, client):
            parsed_token = output[18:32]

            price_and_shares = output.split(":", 3)[3]
            executed_shares = int(price_and_shares.split("@", 1)[0])
            executed_price = int(price_and_shares.split("@", 1)[1])

            print("output={}".format(output))
            cost = executed_price * executed_shares
            print("\nHere is the parsed token:{}\n".format(parsed_token))
            print("\nHere are the executed_shares {}\n".format(executed_shares))
            print("\nHere is the executed_price {}\n".format(executed_price))
            if parsed_token in user.order_tokens and user.order_tokens[parsed_token] == 'B':
                user.cash -= cost
                share_name = [user.bid_stocks[i] for i in user.bid_stocks if i == parsed_token]
                user.inventory[share_name[0]] = executed_shares

            elif parsed_token in user.order_tokens and user.order_tokens[parsed_token] == 'S':
                user.cash += cost
                share_name = [user.ask_stocks[i] for i in user.ask_stocks if i == parsed_token]

                if share_name[0] in user.inventory:
                    user.inventory[share_name[0]] -= executed_shares
                    if user.inventory[share_name[0]] == 0:
                        del user.inventory[share_name[0]]

            client.summary()

        while True:
            message_type = OuchClientMessages.EnterOrder
            for index in itertools.count():
                user_input = await build_message()  #why does this not return a list?
                print(user_input)
                # ['B', 200, 12, 2432, 'Ouch']
                binary_buysell = user_input[0].encode("ascii")
                buy_sell = user_input[0]

                userID = user.get_id()
                tokenID =


                token = '{:014d}'.format(index).encode('ascii')
                token = token.decode('ascii')
                bstock = b'AMAZGOOG'
                stock = bstock.decode('ascii')
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
                     order_token='{:014d}'.format(index).encode('ascii'),
                     buy_sell_indicator=binary_buysell,
                     shares=num_shares,
                     stock=b'AMAZGOOG',
                     price=price,
                     time_in_force=time_in_force,
                     firm=b'OUCH',
                     display=b'N',
                     capacity=b'O',
                     intermarket_sweep_eligibility=b'N',
                     minimum_quantity=1,
                     cross_type=b'N',
                     customer_type=b' ')

                log.info("Sending Ouch message: %s", request)
                await send(request)

                response = await recv()
                log.info("Received response Ouch message: %s:%d", response, len(response))

                while True:
                    try:
                        response = await asyncio.wait_for(recv(), timeout=0.5)
                        log.info("Received response Ouch message: %s:%d", response, len(response))
                        output = str(response)
                        if output[0] == 'E':
                            await update(output, user)
                    except asyncio.TimeoutError:
                        break
                await asyncio.sleep(4.0)

        writer.close()
        asyncio.sleep(0.5)

    loop = asyncio.get_event_loop()
# creates a client and connects to our server
    try:
        loop.run_until_complete(client())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
