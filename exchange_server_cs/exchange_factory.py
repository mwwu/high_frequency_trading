from twisted.internet.protocol import Protocol, ClientFactory
from message_handler import decodeServerOUCH
import matplotlib.pyplot as plt
import time
from collections import OrderedDict 


class Exchange(Protocol):
	def connectionMade(self):
		self.factory.broker.exchange = self
		print("exchange connected")

	def dataReceived(self, data):
		try:
			msg_type, msg = decodeServerOUCH(data) 
			if msg_type == b'A':
				self.factory.graph.plot_accepted_order(msg)
				#hello = 0

			elif msg_type == b'E':
				#print('executed: ', msg)
				self.factory.graph.plot_executed_order(msg)

			elif msg_type == b'Q':
				#print('BBBO: ', msg)
				self.factory.graph.plot_bbbo(msg)

			elif msg_type == b'C':
				#canceled
				hello = 0
			else:
				print('?: ', msg_type)
		except:
			print('EXCEPTION: message type', data)


# handles all data collection and graphing
class ExchangeGrapher():
	def __init__(self, initial_time):
		self.initial_time = initial_time

		self.buyStartTime = []
		self.buyEndTime = OrderedDict()
		self.buyPriceAxis = []

		self.sellStartTime = []
		self.sellEndTime = OrderedDict()
		self.sellPriceAxis = []

		self.crossTime = []
		self.crossPrice = []

		self.bbPrice = []
		self.boPrice = []
		self.bboTime = []

	def plot_accepted_order(self, msg):
		price = msg['price']/10000
		time_in_force = msg['time_in_force']*1000000
		timestamp = msg['timestamp']/1000
		order_token = msg['order_token']

		if msg['buy_sell_indicator'] == b'B':
			self.buyStartTime.append(timestamp)
			self.buyEndTime[order_token] = timestamp + time_in_force
			self.buyPriceAxis.append(price)

		elif msg['buy_sell_indicator'] == b'S':
			self.sellStartTime.append(timestamp)
			self.sellEndTime[order_token] = timestamp + time_in_force
			self.sellPriceAxis.append(price)

	def plot_executed_order(self, msg):
		price = msg['execution_price']/10000
		timestamp = msg['timestamp']/1000
		order_token = msg['order_token']

		self.crossPrice.append(price)
		self.crossTime.append(timestamp)
		if order_token in self.buyEndTime:
			self.buyEndTime[order_token] = timestamp
		if order_token in self.sellEndTime:
			self.sellEndTime[order_token] = timestamp

	def plot_bbbo(self, msg):

		timestamp = msg['timestamp']/1000
		bid_price = msg['best_bid']/10000
		ask_price = msg['best_ask']/10000

		if (ask_price < 200000 and bid_price != 0):
			self.bbPrice.append(bid_price)
			self.boPrice.append(ask_price)
			self.bboTime.append(timestamp)


	def graph_results(self):
		plt.hlines(self.buyPriceAxis, self.buyStartTime, self.buyEndTime.values(), color ="red", linewidth=0.5)
		plt.hlines(self.sellPriceAxis, self.sellStartTime, self.sellEndTime.values(), color ="blue", linewidth=0.5)

		plt.scatter(self.crossTime, self.crossPrice, s=7, linewidth=1, marker = "x")

	def graph_results_bbo(self):
		plt.hlines(self.bbPrice[1:], self.bboTime[:-1], self.bboTime[1:], linewidth=1.5, color="red")
		plt.hlines(self.boPrice[1:], self.bboTime[:-1], self.bboTime[1:], linewidth=1.5, color="blue")


		
	def time(self, time):
		return time - self.initial_time

class ExchangeFactory(ClientFactory):
	protocol = Exchange

	def __init__(self, broker):
		self.broker = broker
		self.graph = ExchangeGrapher(self.broker.initial_time)

	def stopFactory(self):
		self.graph.graph_results()
		plt.title("Market Activity")
		plt.show()

		self.graph.graph_results_bbo()
		plt.title("BBBO Activity")
		plt.show()
