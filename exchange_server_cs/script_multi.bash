xterm -hold -e python3 run_exchange_server.py --host 0.0.0.0 --port 9001 --debug --mechanism cda &
xterm -hold -e python3 run_exchange_server.py --host 0.0.0.0 --port 9002 --debug --mechanism cda &
xterm -hold -e python3 broker.py &
xterm -hold -e python3 broker2.py &
xterm -hold -e python3 external_clients.py &
xterm -hold -e python3 external_clients2.py &
xterm -hold -e python3 both_market_external_clients.py 

