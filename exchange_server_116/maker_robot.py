#~Bid_i(t) = BB_i - S * B(x(t), y(t))
#~Ask_i(t) = BO_i + S * A(x(t), y(t))


#Bid = min{[~Bid]s, BO - 2S}
#Ask = max{[~Ask]s, BB + 2S}



##
#create a robot  [X]

#connect to the proxy server []
# receive execute message and parse it [X]
# update robot's cash and inventory [X]
# Receive BA and BO []
# price = formulas above ^ [X]

# create messages []

# Send new message []
#

from hft import equations
from __future__ import print_function

# import make_connection
from exchange_server_116.make_connection import Greeter
from exchange_server_116.make_connection import gotProtocol
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from exchange_server_116.OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

#import make_connection
from exchange_server_116.make_connection import Greeter
from exchange_server_116.make_connection import gotProtocol

aggressiveness = 0.5
b_x = 0.5 #slider 
b_y = 0.5 #slider 

a_x = 0.5 #slider 
a_y = 0.5 #slider 

x = 1 #get from broker 
y = 1 #get from broker


S_CONST = 1

class Maker_Client:
	def __init__(self, cash, id):
		self.id = id
		self.cash = cash
		self.inventory = {}
		self.order_tokens = {}  # key = order token and value = 'B' or 'S'
		self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
		self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
		self.bid_quantity = {}
		self.ask_quantity = {}
		self.best_bid = 0
		self.best_offer = 0
		self.bid_i = 0
		self.ask_i = 0
		self.point = TCP4ClientEndpoint(reactor, "localhost", 8000)
		self.test = 0

	def get_id(self):
		return self.id

	def get_cash(self):
		return self.cash

	def get_inventory(self):
		return self.inventory

	def new_ask(self):
		ask_price = self.best_bid - S_CONST * aggressiveness
		self.ask_i = ask_price
		return ask_price

	def new_bid(self):
		bid_price = self.best_offer - S_CONST * aggressiveness
		self.bid_i = bid_price
		return bid_price

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


	def update_cash_inventory(self, output):
		parsed_token = output[18:32]

		price_and_shares = output.split(":", 3)[3]
		executed_shares = int(price_and_shares.split("@", 1)[0])
		executed_price = int(price_and_shares.split("@", 1)[1])

		print("output={}".format(output))
		cost = executed_price * executed_shares
		print("\nHere is the parsed token:{}\n".format(parsed_token))
		print("\nHere are the executed_shares {}\n".format(executed_shares))
		print("\nHere are the executed_price {}\n".format(executed_price))
		if parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'B':
			self.cash -= cost
			share_name = [self.bid_stocks[i] for i in self.bid_stocks if i == parsed_token]
			self.inventory[share_name[0]] = executed_shares

		elif parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'S':
			self.cash += cost
			share_name = [self.ask_stocks[i] for i in self.ask_stocks if i == parsed_token]

		if share_name[0] in self.inventory:
			self.inventory[share_name[0]] -= executed_shares
		if self.inventory[share_name[0]] == 0:
			del self.inventory[share_name[0]]


	def bid_aggressiveness(b_x, b_y, x, y):
		"""
		B(x(t), y(t))
		x: order imbalance
		y: inventory position
		"""
		return - b_x * x + b_y * y

	def sell_aggressiveness(a_x, a_y, x, y):
		"""
		A(x(t), y(t))
		x: order imbalance
		y: inventory position
		"""
		return a_x * x - a_y * y


	def latent_bid(bb, S, bid_aggressiveness):
		"""
		LB(t)
		bb: best bid
		S: half a tick
		"""
		return bb - S * bid_aggressiveness

	def latent_offer(bo, S, sell_aggressiveness):
		"""
		LB(t)
		bb: best offer
		S: half a tick
		"""
		return bo + S * sell_aggressiveness

	def connect(self):
		print("Trying to connect ...\n")
		d = connectProtocol(self.point, Greeter())
		self.test = d
		print("111111111111111\n")
		d.addCallback(gotProtocol)
		print("22222222222\n")
		reactor.run()

	def build_Message(self):
		#parameters: buy/sell and price
		message_type = OuchClientMessages.EnterOrder

		request = message_type(
			order_token='{:014d}'.format(1000).encode('ascii'),
			buy_sell_indicator='B',
			shares=10,
			stock=b'AMAZGOOG',
			price=1000,
			time_in_force=10000,
			firm=b'OUCH',
			display=b'N',
			capacity=b'O',
			intermarket_sweep_eligibility=b'N',
			minimum_quantity=1,
			cross_type=b'N',
			customer_type=b' ')
	    self.test = Greeter.sendMessage(request)



