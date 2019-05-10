from twisted.internet import reactor
import time

from clients_factory import ClientsFactory
from exchange_factory import ExchangeFactory
from underlying_value import UnderlyingValue



class Broker():
	def __init__(self):
		self.initial_time = time.time()

		self.clients = []
		self.exchange = None
		self.underlyingValueFeed = UnderlyingValue(self.time, self.clients)

	def data_recieved_from_client(self, data):
		print(data)

	def data_recieved_from_exchange(self, data):
		print(data)

	def time(self):
		return time.time() - self.initial_time


def main():
	broker = Broker()

	reactor.connectTCP("localhost", 9001, ExchangeFactory(broker))
	reactor.listenTCP(8000, ClientsFactory(broker))

	reactor.callLater(10, reactor.stop)
	reactor.run()

if __name__ == '__main__':
    main()