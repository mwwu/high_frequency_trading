from enum import Enum

class OrderStatus(Enum):
    UNCONFIRMED = "Unconfirmed" #order has been sent out
    CONFIRMED = "Confirmed" #order has been received by server
    UPDATED = "Updated" #client sent an updated order, change to confirmed once server responds
    EXECUTED = "Executed" #order has been executed by server

class OrderType(Enum):
    BUY = "Buy"
    SELL = "Sell"