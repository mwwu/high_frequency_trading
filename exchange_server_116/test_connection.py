
from exchange_server_116.maker_robot import Maker_Client

#import maker_robot

#roboti = Maker_Clinet(Cash, id)
print("inside test_connection")
robot1 = Maker_Client(0, 1)
robot1.connect()
robot1.buildMessage()
print("exiting test_connection")

