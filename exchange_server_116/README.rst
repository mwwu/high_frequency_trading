...............

1. Run the exchange server
::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

2. Run the broker
::

	python3 test_broker.py

3. Run the traders (can run multiple at same time). The Test trader sends 4 random trades. The random trader sends 4 poisson distributed trades. The maker trader responds to BB and BO live feed updates, and sends trades based on academic paper equations.
::
	python3 test_trader_client.py 
	python3 random_trader_client.py
	python3 maker_trader_client.py
