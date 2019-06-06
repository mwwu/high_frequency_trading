Note: Using python 3.7

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



=====
Intro
=====
This is a software project between our group(from CMPS116 + CMPS117) and the LEEPS Lab (from the UCSC Economic Department, main contact: Prof Kristian Lopez Vargas). The goal of the project was to create a stock market simulation in order for LEEPS to develop, and rigorously test, a new type of stock market. This document will describe the current state of the project, as well as unachieved goals, in order to help the next group quickly pick up where we left off. 

===============
Getting Started
===============

Step 0
***********
In order to run the system, you will first need to install the requirements. Open bash / terminal and type:
::
	pip3 install -r requirements.txt


Step 1
***********
By the time our project started, LEEPS had already built two types of stock markets: CDA and FBA. To learn about the differences between these markets, read the paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3154070. (Ask the Professor for a more recent edition, because they have already made a few changes.) 

Open a new terminal window and start the CDA Exchange. Type this:
::
	python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda

OR start the FBA Exchange:
::
	python3 run_exchange_server.py --host 0.0.0.0 --port 9101 --debug --mechanism fba --interval 3
	
Step 2
***********	
In order to keep track of all of the communications between the traders and the exchange, we created a Broker. When we start the Broker, you should see some activity in the Exchange window. This lets us know that the Broker has successfully connected to the Exchange. 

(Optional) Open a new terminal window, and start the Broker:
::
	python3 broker.py


Step 3
***********
Now that the Broker is running, it is ready to receive and forward orders to the Exchange. We created Traders to generate these orders. A Trader's only job is to decide what price they want to buy or sell a stock for. Let's start buying and selling stocks.

Open a new terminal window, and start a Trader:
::
	python3 external_clients.py 
	
	
Ready!
***********
These three types of components make up the entire system (Exchange, Broker, and Trader). Further into this documentation, we will describe each component in detail, as well as how they communicate with each other.


===============
Background Info
===============
In order to understand this project, there are many things you will need to get familiar with, both in coding and economics. Below is a list of concepts that we encountered the most, as well as questions you should be able to answer (some of these took us the full 6 months to understand). 

Stock Market: Handling Orders
*********************************
- What is the "book" and how does it work?
- What happens in the Exchange when a trader submits a Buy order? 
- What happens in the Exchange when a trader submits a Sell order?
- What happens when a Buy order and a Sell order "cross" with each other?
- Draw a diagram of the book as Buy and Sell orders are placed.
- What is the Best Bid and Best Offer? (Circle this in your diagram)

Stock Market: High Frequency Trading
******************************************
- https://faculty.chicagobooth.edu/eric.budish/research/HFT-FrequentBatchAuctions.pdf
- What is high frequency trading?
- Suppose we have two traders (one HFT, and one normal trader). Draw a diagram of how HFT makes profits.
- Why is HFT considered unfair?
- What is latency, and how does HFT take advantage of it?
- How does HFT affect the price of a stock?

Stock Market: Types of Markets
************************************
- Background Reading: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3154070
- What is a CDA, and how does it handle orders?
- What is an FBA, and how does it handle orders?
- Which one is hypothesized to help, 



TODO ----------------

- Basic understanding of how the stock market works (Read the Stock Market section below, ask the Prof, 
- how the stock market book works
- python
- twisted
- how servers and ports work

===============
Exchange
===============
- the broker consists of feeds
- what is underlying value

===============
Broker
===============
- the broker consists of feeds
- what is underlying value


===============
Traders
===============
- the broker consists of feeds
- what is underlying value
