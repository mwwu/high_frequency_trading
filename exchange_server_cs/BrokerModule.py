from twisted.internet import reactor
import time

from clients_factory import ClientsFactory
from exchange_factory import ExchangeFactory
from underlying_value import UnderlyingValue


"""
Broker Class:
- only handles routing and timing functionalities
- this class wont need to know the details about the actual orders it handles
"""
class BrokerModule():

	def data_recieved_from_exchange(self, data):
		print(data)
		#hello = None

def main():
	broker = Broker()

	reactor.listenTCP(8000, ClientsFactory(broker))
	reactor.listenTCP(8001, ClientsFactory(broker))

	#reactor.connectTCP("localhost", 9001, ExchangeFactory(broker))
	#reactor.connectTCP("localhost", 9002, ExchangeFactory(broker))

	#reactor.callLater(120, reactor.stop)
	#reactor.run()

if __name__ == '__main__':
	main()
