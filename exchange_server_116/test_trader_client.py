from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
from OuchServer.ouch_messages import OuchClientMessages
from random import randrange
import time
from message_handler import decodeServerOUCH, decodeClientOUCH

# -----------------------
# TraderClient class: sends orders to the broker
# -----------------------
class TraderClient(Protocol):

	def connectionMade(self):
		reactor.callLater(0, self.sendBuyOrder)
		reactor.callLater(4, self.sendSellOrder)
		#reactor.callLater(8, self.sendOrder)
		#reactor.callLater(12, self.sendOrder)

	def sendBuyOrder(self):
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

	def sendSellOrder(self):
		order = OuchClientMessages.EnterOrder(
			order_token='{:014d}'.format(0).encode('ascii'),
			buy_sell_indicator=b'S',
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
		else:
			msg_type, msg = decodeServerOUCH(data)
			print("SERVER SAYS: ", msg)


# -----------------------
# Main function
# -----------------------
def main():
    traderClientFactory = ClientFactory()
    traderClientFactory.protocol = TraderClient
    reactor.connectTCP("localhost", 8000, traderClientFactory)
    reactor.run()

if __name__ == '__main__':
    main()
