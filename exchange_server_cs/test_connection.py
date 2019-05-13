
from maker_robot import Maker_Client
from twisted.internet import protocol
from twisted.internet import reactor

from twisted.internet import task

#import maker_robot
"""
#roboti = Maker_Clinet(Cash, id)
print("inside test_connection")
robot1 = protocol.ClientFactory
robot1.protocol = Maker_Client(1, 0)
robot1.protocol.connect()
msg = robot1.protocol.build_Message()
robot1.protocol.connectionMade(msg)
print("exiting test_connection")
"""
def main(reactor):
  factory = protocol.ClientFactory()
  factory.protocol = Maker_Client(1, 0)
  reactor.connectTCP('localhost', 8000, factory)
  msg = factory.protocol.build_Message()
  #factory.protocol.connectionMade(msg)
  return  factory.done
#reactor.run()

if __name__ == '__main__':
  task.react(main)
