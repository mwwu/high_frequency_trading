Note: Using python 3

Dependencies:

::

    pip3 install -r requirements.txt

To run a CDA instance:

::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda
    
To run a FBA instance with batch length of 3 seconds:

::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9101 --debug --mechanism fba --interval 3


...............

1. run the exchange server
::

        $: python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

2. run the broker
::

	$: python3 broker.py
	
3. Specify what trader to use in external_clients.py
::

	open external_clients.py 
	Under the "Specify Trader" comment on line 16:
	either write ' self.trader = RandomTrader.RandomTrader(self) '
	or '  self.trader = MakerTrader.MakerTrader(self) '
	without the single quotes.


4. run the traders (can run multiple at same time)
::
	$: python3 external_clients.py 
	

What it does: As soon as a trader is connected, it will send an Order to the Broker, which forwards it to the Exchange. The Exchange will then send a response to the Broker. TODO: the message is a wierd bytes/hex/ascii thing that I cant decode yet
