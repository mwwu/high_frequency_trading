Dependencies:

::

    pip install -r requirements.txt

To run a CDA instance:

::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda
    
To run a FBA instance with batch length of 3 seconds:

::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9101 --debug --mechanism fba --interval 3


...............

1. run the exchange server
::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

2. run the broker
::

	python3 test_broker.py

3. run the traders (can run multiple at same time)
::
	python3 test_trader_client.py 
	python3 random_trader_client.py
	python3 maker_trader_client.py

What it does: As soon as a trader is connected, it will send an Order to the Broker, which forwards it to the Exchange. The Exchange will then send a response to the Broker. TODO: the message is a wierd bytes/hex/ascii thing that I cant decode yet