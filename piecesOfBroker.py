#1. parse the message into our database from the server / no longer client

# assume the message we received from server is E:00000000000000:B44xAMAZGOOG@33 for executedOrder
# A means confirmed, and we should add it to the book
text1 = data.decode()
token = text1.split(':')
if (token[2][0] == 'B'):
  temp = token[2].split('B')
else:
  temp = token[2].split('S')
qShares = temp[1].split('x')
stockN = qShares[1].split('@')

# setting variables so that it is more readable
orderStatus = token[0]
orderID = token[1]
buySell = token[2][0] # buying or selling
stockPrice = stockN[1] 
stockName = stockN[0]
quantityShares = qShares[0]

# ------------------------------------------------------------------

# appending to the book if order has been confirmed
if (orderStatus == 'A'):
    self.stock[orderID] = stockName
    self.quantity[orderID] = quantityShares
    # if it's a bid add it to the quantities bidded to the sumBB
    if (buySell == 'B'):
        self.buyStock[orderID] = stockPrice
        # if not yet in dictionary set default of quantity to 0
        self.sumBB.setdefault(stockPrice, default=0)
        # update the sum at the stockPrice
        self.sumBB[stockPrice] = self.sumBB[stockPrice]+quantityShares
    # else it's an offer add it to the quantities offered to the sumBO
    else:
        self.sellStock[orderID] = stockPrice
        self.sumB0.setdefault(stockPrice, default=0)
        self.sumB0[stockPrice] = self.sumBB[stockPrice]+quantityShares
# if the order is executed, eliminate the quanities of shares it crossed with
else if (orderStatus == 'E'):
    # is the orderID from the executed message already in the book or not?
    #   assuming that it is in the book, we will update it as it has crossed with another,
    #   by deleting the quantity that it was crossed with
    if (orderID in self.buyStock):
        # subtract the quantity from the quantity of its sum at this price
        self.sumBB[self.buyStock[orderID]] = self.sumBB[self.buyStock[orderID]] - self.quantity[orderID]
        if (self.sumBB[self.buyStock[orderID]] == 0):
            del self.sumBB[self.buyStock[orderID]]
    else:
        self.sumBO[self.buyStock[orderID]] = self.sumBO[self.buyStock[orderID]] - self.quantity[orderID]
        if (self.sumBO[self.buyStock[orderID]] == 0):
            del self.sumBO[self.buyStock[orderID]]
    # eliminate the quantities crossed with the quantity stored in this orderID
    self.quantity[orderID] = self.quantity[orderID] - quantityShares 
    if (self.quantity[orderID] == 0): # if the quantity is 0, delete it from the book
        del self.quantity[orderID]
        del self.stock[orderID]
        if (buySell == 'B'):
            del self.buyStock[orderID]
        else:
            del self.sellStock[orderID]

# ------------------------------------------------------------------


# organizes all the bids from greatest to least
# organizes all the offers from least to greatest
listOfBB = []
listOfBO = []
for i in sorted(self.sumBB.keys(), reverse=True):
    listOfBB.append(sumBB[i])
for i in sorted(self.sumBO.keys()):
    listOfBB.append(sumB0[i])

# factory.client holds all the client's orderID
iteratorForBB = 0 # used to iterate through the listOfBB/listOfBO
iteratorForBO = 0
theirBBQ, theirBOQ = 0 # best bid quantity/best offer quantity
for clientID in self.factory.clients:
    if (clientID in self.buyStock):
        # if the their bid is equal to the best bid
        # set theirBBQ to the quantity of the best bid 
        if (self.buyStock[clientID] == listofBB[iteratorForBB]):
            theirBBQ = self.sumBB[clientID] - self.quantity
            # if the quantity ends up being 0 move the iterator to the next best bid
            if (theirBBQ == 0):
                iteratorForBB++
    else if (clientID in self.sellStock):
        if (self.sellStock[clientID] == listofBO[iteratorForBO]):
            theirBBO = self.sumBO[clientID] - self.quantity
            if (theirBOQ == 0):
                iteratorForBO++

print("Your best bid is " + listofBB[iteratorForBB] + " with " + self.sumBB[listofBB[iteratorForBB]] + "shares.")
print("Your best offer is " + listofBO[iteratorForBO] + " with " + self.sumBO[listofBO[iteratorForBO]] + "shares.")


# --------------------------------------------------------------------

# initially
order_imbalance = 0
tau = 0

# in the dataReceived function
tau = currentTime - tau
if (orderStatus == 'E'):
    if (exchange price = BO):
        order_imbalance = e*(p*tau)*order_imbalance + 1
    else if (exchange price = BB):
        order_imbalance = e*(p*tau)*order_imbalance - 1
    else:
        order_imbalance = e*(p*tau)*order_imbalance
