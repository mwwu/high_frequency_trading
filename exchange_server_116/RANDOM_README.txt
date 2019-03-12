1. First install numpy dependency: (using the version appropriate for your operating system).
	
	python -m pip install numpy
 
2. To run a CDA instance:

::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

3. To run a client: python random_station.py <max_id>, where max_id is the desired number of clients between 1 and 9999.