from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import time
from message_handler import decodeServerOUCH, decodeClientOUCH
from inventory import Inventory

# TODO: not working yet!!

S = 1
aggressiveness = 0.5
b_x = 0.5 #slider 
b_y = 0.5 #slider 

a_x = 0.5 #slider 
a_y = 0.5 #slider 

x = 1 #get from broker 
y = 1 #get from broker

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

# -----------------------
# MakerTraderClient class: sends orders to the broker
# -----------------------
class MakerTraderClient(Protocol):
	def __init__(self, inventory):
		self.inventory = inventory
		
	def connectionMade(self):
		print("maker connected")
		#reactor.callLater(0, self.sendBuyOrder)
		#reactor.callLater(4, self.sendSellOrder)
		#reactor.callLater(8, self.sendOrder)
		#reactor.callLater(12, self.sendOrder)

	def sendOrder(self):
		order = OuchClientMessages.EnterOrder(
			order_token='{:014d}'.format(0).encode('ascii'),
			buy_sell_indicator=b'B',
			shares=randrange(1,10**6-1),
			stock=b'AMAZGOOG',
			price=randrange(1,10**9-100),
			time_in_force=randrange(0,99999),
			firm=b'OUCH',
			display=b'N',
			capacity=b'O',
			intermarket_sweep_eligibility=b'N',
			minimum_quantity=1,
			cross_type=b'N',
			customer_type=b' ')
		self.transport.write(bytes(order))


	def dataReceived(self, data):
		ch = chr(data[0]).encode('ascii')
		if (ch == b'#'):
			print("BB/BO: ", data)
			reactor.callLater(0, self.sendOrder)
		else:
			msg_type, msg = decodeServerOUCH(data)
			if msg_type == b'A':
				self.inventory.confirmedOrder(
					msg['order_token'], 
					msg['buy_sell_indicator'], 
					msg['shares'], 
					msg['price']
				)

			elif msg_type == b'E':
				print('executed order')
				self.inventory.executedOrder(
					msg['order_token'], 
					msg['executed_shares']
				)
			self.inventory.printCurrentPositionDetailed()


# -----------------------
# Main function
# -----------------------
def main():
	inventory = Inventory(100, 1)
	def protocol():
		return MakerTraderClient(inventory)

	factory = ClientFactory()
	factory.protocol = protocol
	reactor.connectTCP("localhost", 8000, factory)
	reactor.run()

if __name__ == '__main__':
    main()
