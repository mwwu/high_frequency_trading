"""
Client for simple Ouch Server
"""
from client import Client
from maker_robot import Maker
def main():
  print("BUILD CLIENT")
  trader1 = Client("Maker")
  maker_instance = Maker(trader1)
  #trader1.run_algorithm

if __name__ == '__main__':
    main()
