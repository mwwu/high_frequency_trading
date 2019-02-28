#~Bid_i(t) = BB_i - S * B(x(t), y(t))
#~Ask_i(t) = BO_i + S * A(x(t), y(t))


#Bid = min{[~Bid]s, BO - 2S}
#Ask = max{[~Ask]s, BB + 2S}



##
#create a robot  [X]

#connect to the proxy server []
# receive execute message and parse it [X]
# update robot's cash and inventory [X]
# Receive BA and BO []
# price = formulas above ^ [X]

# create messages []

# Send new message []
#

aggressiveness = 0.5
S_CONST = 1

class Maker_Client:
    best_bid = 0
    best_offer = 0
    bid_i = 0
    ask_i = 0
    def __init__(self, cash, id):
        self.id = id
        self.cash = cash
        self.inventory = {}
        self.order_tokens = {}  # key = order token and value = 'B' or 'S'
        self.bid_stocks = {}  # stocks that you are bidding in market  key=order token and value = stock name
        self.ask_stocks = {}  # same as bid_stocks for key and value, this is needed cause executed messages dont return stock name
        self.bid_quantity = {}
        self.ask_quantity = {}
        self.best_bid = best_bid
        self.best_offer = best_offer
        self.bid_i = bid_i
        self.ask_i = ask_i

    def get_id(self):
        return self.id

    def get_cash(self):
        return self.cash

    def get_inventory(self):
        return self.inventory

    def new_ask(self):
        ask_price = self.best_bid - S_CONST * aggressiveness
        self.ask_i = ask_price
        return ask_price

    def new_bid(self):
        bid_price = self.best_offer - S_CONST * aggressiveness
        self.bid_i = bid_price
        return bid_price

    # Task 6: Add and Withdraw Cash from Wallet
    def add_withdraw_cash(self):
        print("Do you want to add or withdraw cash? ")
        while (1):
            add_or_withdraw = input("Type A for add and W for withdraw. ")
            if (add_or_withdraw == 'A'):
                add = input("How much money do you want to add? ")
                self.cash += int(add)
                break;
            elif (add_or_withdraw == 'B'):
                sub = input("How much money do you want to withdraw? ")
                self.cash -= int(sub)
                break;
            else:
                print("Please try again.")

    def update_cash_inventory(self, output):
            parsed_token = output[18:32]

            price_and_shares = output.split(":", 3)[3]
            executed_shares = int(price_and_shares.split("@", 1)[0])
            executed_price = int(price_and_shares.split("@", 1)[1])

            print("output={}".format(output))
            cost = executed_price * executed_shares
            print("\nHere is the parsed token:{}\n".format(parsed_token))
            print("\nHere are the executed_shares {}\n".format(executed_shares))
            print("\nHere are the executed_price {}\n".format(executed_price))
            if parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'B':
                self.cash -= cost
                share_name = [self.bid_stocks[i] for i in self.bid_stocks if i == parsed_token]
                self.inventory[share_name[0]] = executed_shares

            elif parsed_token in self.order_tokens and self.order_tokens[parsed_token] == 'S':
                self.cash += cost
                share_name = [self.ask_stocks[i] for i in self.ask_stocks if i == parsed_token]

                if share_name[0] in self.inventory:
                    self.inventory[share_name[0]] -= executed_shares
                    if self.inventory[share_name[0]] == 0:
                        del self.inventory[share_name[0]]

def main():
    robot1 = Maker_Client(0, 1)
