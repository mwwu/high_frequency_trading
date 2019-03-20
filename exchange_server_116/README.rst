Original LEEPS Instructions

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

116 Instructions 

0. Go to testing_broker branch

1. run the exchange server
::

    python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

2. run the broker
::

	python3 test_broker.py

3. run the traders (can run multiple at same time)
::
	python3 test_trader_client.py

What it does: As soon as a trader is connected, it will send an Order to the Broker, which forwards it to the Exchange. The Exchange will then send a response to the Broker. TODO: the message is a wierd bytes/hex/ascii thing that I cant decode yet


...............

Acceptance Test Instructions (from Jullig Piazza)

My goal for the project reviews is to understand:

 

1. the goal and scope of your entire project (as you currently understand it)

    i.e. be prepared to give a pithy description of the Why and What of your project

 

2. the current status of your project

    i.e. be prepared to give a comprehensible, quasi-realistic demo of your system, explain key system design and technology choices, and show key sections of the code base

 

3. the project management practices you employed

   i.e. be prepared to describe your process and show associated documents (release and sprint plans, sprint reports, minutes of meetings, etc. (If you don't have some of these documents, don't make them up now.)

 

4. the individual contributions of the team members

   i.e. be prepared to characterize and summarize your contributions to the project

 

5. the project goals for cmps117

   i.e. describe the product you plan to achieve by the end of cmps117 and the key aspects of the work necessary to get there (a preview of your cmps117 release plan).

 

Cheers,

Richard J.
