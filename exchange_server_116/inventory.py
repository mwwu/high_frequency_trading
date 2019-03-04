from exchange_server_116.state import OrderStatus, OrderType

## inventory class
class Inventory:
    def __init__(self, cash, id):
        self.id = id
        self.cash = cash
        self.inventory = {} # what stocks we have/own, key = stockname, value = quantity

        ##### LIVE ORDERS ######
        self.status = {} # key is orderID, value is status
        self.stock = {} # key is orderID, value is stocks
        self.orderType = {} # key is orderID, value is order type B or S
        self.price = {} # key is orderID, value is price
        self.quantity = {}  # key is orderID, value is quantity
        self.timestamp = {} # key is orderID, value is timestamp
        ##### LIVE ORDERS ######

    def unconfirmedOrder(self, stock, orderType, price, quantity, orderID):
        self.status[orderID] = OrderStatus.UNCONFIRMED
        self.stock[orderID] = stock
        self.orderType[orderID] = orderType
        self.price[orderID] = price
        self.quantity[orderID] = quantity

    def confirmedOrder(self, orderID):
        self.status[orderID] = OrderStatus.CONFIRMED

    def updatedOrder(self, stock, orderType, price, quantity, orderID):
        self.status[orderID] = OrderStatus.UPDATED
        self.stock[orderID] = stock
        self.orderType[orderID] = orderType
        self.price[orderID] = price
        self.quantity[orderID] = quantity

    def executedOrder(self, orderID):
        stock = self.stock[orderID]
        orderType = self.orderType[orderID]
        price = self.price[orderID]
        quantity = self.quantity[orderID]

        if (orderType == OrderType.BUY):
            self.inventory[stock] = self.inventory.get(stock, 0) + quantity
            self.cash -= (price * quantity)
        elif (orderType == OrderType.SELL):
            self.inventory[stock] = self.inventory.get(stock, 0) - quantity
            self.cash += (price * quantity)

        del self.status[orderID]
        del self.stock[orderID]
        del self.orderType[orderID]
        del self.price[orderID]
        del self.quantity[orderID]

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
        print("Current Cash:{}\n".format(self.cash))
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
                    self.orderType[orderID].value,
                    self.quantity[orderID], "x",
                    self.stock[orderID],
                    "@", self.price[orderID])
        print("-------------------")
