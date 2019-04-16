from state import OrderStatus, OrderType

## inventory class
class Inventory:
    def __init__(self, cash, id):
        self.id = id
        self.cash = cash
        self.inventory = {} # what stocks we have/own, key = stockname, value = quantity

        ##### LIVE ORDERS ######
        self.status = {} # key is orderID, value is status
        self.orderType = {} # key is orderID, value is order type B or S
        self.shares = {}  # key is orderID, value is quantity
        self.price = {} # key is orderID, value is price
        #self.timestamp = {} # key is orderID, value is timestamp
        ##### LIVE ORDERS ######

    def confirmedOrder(self, order_token, buy_sell_indicator, shares, price):
        self.status[order_token] = OrderStatus.CONFIRMED
        self.orderType[order_token] = buy_sell_indicator
        self.shares[order_token] = shares
        self.price[order_token] = price

    def updatedOrder(self, stock, orderType, price, shares, orderID):
        self.status[orderID] = OrderStatus.UPDATED
        self.stock[orderID] = stock
        self.orderType[orderID] = orderType
        self.price[orderID] = price
        self.shares[orderID] = shares

    def executedOrder(self, order_token, executed_shares):
        print("order token: ", order_token)
        orderType = self.orderType[order_token]
        shares = self.shares[order_token] - executed_shares
        stock = "AMAZGOOG"
        price = self.price[order_token]


        if (orderType == b'B'):
            self.inventory[stock] = self.inventory.get(stock, 0) + executed_shares
            self.cash -= (price * executed_shares)
        elif (orderType == b'S'):
            self.inventory[stock] = self.inventory.get(stock, 0) - executed_shares
            self.cash += (price * executed_shares)

        if (shares <= 0):
            del self.status[order_token]
            del self.orderType[order_token]
            del self.shares[order_token]
            del self.price[order_token]


    # y(t) = sum of the quantity
    def inventoryPosition(self):
        return sum(self.inventory.values())

    # add / withdraw cash (copy from prev document)
    def depositCash(self, amount):
        self.cash = self.cash + amount

    def withdrawCash(self, amount):
        self.cash = self.cash - amount

    # print function
    def printCurrentPosition(self):
        print("\nCurrent Cash:{}\n" "Current Quantity:{} \n"
            .format(self.cash, self.inventoryPosition()))

    def printCurrentPositionDetailed(self):
        print("Current Cash: ", self.cash)
        print("Current Inventory:")
        if not self.inventory:
            print("Empty\n")
        else:
            for stock in self.inventory:
                print(stock, "x", self.inventory[stock])
        print("Current Orders:")
        if not self.status:
            print("No Orders")
        else:
            for orderID in self.status:
                print(orderID, "|",
                    self.status[orderID].value,
                    self.orderType[orderID],
                    self.shares[orderID], "xAMAZGOOG",
                    "@", self.price[orderID])
        print("-------------------")
