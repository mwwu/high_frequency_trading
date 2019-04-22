"""
Client for simple Ouch Server
"""
from client import *
from maker_robot import Maker

def main():
  print("BUILD CLIENT")

  trader1 = Client("Maker")
  print("\n... trader1 = Client(\"Maker\") executed ...\n")

  trader1.connect_client()  
  print("\n... trader1.connect_client executed ...\n")
  maker_instance = Maker(trader1)
  print("\n... maker_instance = Maker(trader1) executed ...\n")

  maker_instance.begin_maker()
  print("\n... maker_instance.begin_maker() executed ...\n")

  #trader1.run_algorith

if __name__ == '__main__':
    main()
