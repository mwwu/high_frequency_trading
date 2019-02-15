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

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

p = configargparse.ArgParser()
p.add('--port', default=9001)
p.add('--host', default='127.0.0.1', help="Address of server")
options, args = p.parse_known_args()

def main():
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

        # send a line
        while True:
            message_type = OuchClientMessages.EnterOrder
            for index in itertools.count():
                message_type = OuchClientMessages.EnterOrder
                input_array = build_message()
                request = message_type(
                    order_token='{:014d}'.format(index).encode('ascii'),
                    buy_sell_indicator=bytes(input_array[0], 'ascii'),
                    shares=input_array[1],
                    stock=b'AMAZGOOG',
                    price=input_array[2],
                    time_in_force=input_array[3],
                    firm=bytes(input_array[4], 'ascii'),
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
                await asyncio.sleep(4.0)

        writer.close()
        await asyncio.sleep(0.5)


    loop = asyncio.get_event_loop()

    # creates a client and connects to our server
    try:
        loop.run_until_complete(client())
    finally:
        loop.close()

def build_message():
    print("Type q to start again")
    buy_sell_builder = verify_buy_sell()
    shares_builder = verify_shares(buy_sell_builder)
    price_builder = verify_price(buy_sell_builder, shares_builder)
    time_in_force_builder = verify_time()
    firm_builder = verify_firm(buy_sell_builder)
    return[buy_sell_builder, shares_builder, price_builder, time_in_force_builder, firm_builder]

def verify_buy_sell():
    print("Type B to buy or S to sell")
    buy_sell_input = input()
    if (buy_sell_input == 'q'):
        build_message()
    elif (buy_sell_input == 'B' or buy_sell_input == 'S'):
        return buy_sell_input
    else:
        print("Type B for buy, S for sell or q to start again:")
        verify_buy_sell()

def verify_shares(buy_sell_builder):
    print("Number of shares: more than 0, less than a million")
    shares_input = input()
    if(shares_input == 'q'):
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

def verify_price(buy_sell_builder, shares_builder):
    print("Provide the price at which you are happy to trade:")
    price_input = input()
    # Check if the price is an integer:
    try:
        price_int = int(price_input)
    except ValueError:
        print("You need to provide an integer.")
        verify_price(buy_sell_builder, shares_builder)
    # Check if price is in the range:
    if (price_int<0 or price_int>(10**9-100)):
        print("You provided a value outside of range.")
        verify_price(buy_sell_builder, shares_builder)
    else:
        # if(buy_sell_builder == 'B'):
        #     if (price_int * shares_builder > seller.getPrice()):
        #         print("You don't have enough cash in your wallet")
        #         verify_price()
        return price_int

def verify_time():
    print("Provide the time in force; minimum 0, max 99999")
    time_in_force_input = input()
    #time_in_force=randrange(0,99999)
    try:
        time_int = int(time_in_force_input)
    except ValueError:
        print("You need to provide an integer.")
        verify_time()
    if(time_int < 0 or time_int > 99999):
        print("You provided the time outside of range.")
        verify_time()
    else:
        self.inventory[share] -= amt
        self.cash += amt*price

# Tasks 1 and 5
def build_message():
    print("Type q to start again")
    buy_sell_builder = verify_buy_sell()
    shares_builder = verify_shares(buy_sell_builder)
    price_builder = verify_price(buy_sell_builder, shares_builder)
    time_in_force_builder = verify_time()
    firm_builder = verify_firm(buy_sell_builder)
    return[buy_sell_builder, shares_builder, price_builder, time_in_force_builder, firm_builder]

def verify_buy_sell():
    print("Type B to buy or S to sell")
    buy_sell_input = input()
    if (buy_sell_input == 'q'):
        build_message()
    elif (buy_sell_input == 'B' or buy_sell_input == 'S'):
        return buy_sell_input
    else:
        print("Type B for buy, S for sell or q to start again:")
        verify_buy_sell()

def verify_shares(buy_sell_builder):
    print("Number of shares: more than 0, less than a million")
    shares_input = input()
    if(shares_input == 'q'):
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

def verify_price(buy_sell_builder, shares_builder):
    print("Provide the price at which you are happy to trade:")
    price_input = input()
    # Check if the price is an integer:
    try:
        price_int = int(price_input)
    except ValueError:
        print("You need to provide an integer.")
        verify_price(buy_sell_builder, shares_builder)
    # Check if price is in the range:
    if (price_int<0 or price_int>(10**9-100)):
        print("You provided a value outside of range.")
        verify_price(buy_sell_builder, shares_builder)
    else:
        # if(buy_sell_builder == 'B'):
        #     if (price_int * shares_builder > seller.getPrice()):
        #         print("You don't have enough cash in your wallet")
        #         verify_price()
        return price_int

def verify_time():
    print("Provide the time in force; minimum 0, max 99999")
    time_in_force_input = input()
    #time_in_force=randrange(0,99999)
    try:
        time_int = int(time_in_force_input)
    except ValueError:
        print("You need to provide an integer.")
        verify_time()
    if(time_int < 0 or time_int > 99999):
        print("You provided the time outside of range.")
        verify_time()
    else:
        return time_int

def verify_firm(buy_sell_builder):
    print("What firm are you trading for:")
    firm_input = input()
    # if (buy_sell_builder == 'S'):
    #     if not firm_input.belongsTo(portfolio):
    #         print("You don't have this firm")
    return firm_input

# Task 6: Add and Withdraw Cash from Wallet
def add_withdraw_cash(self):
    print("Do you want to add or withdraw cash? ")
    add_or_withdraw = input("Type A for add and W for withdraw. ")
    while(1):
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


main()
