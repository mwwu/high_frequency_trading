

order_imbalance = 0
tau = 0

def dataReceived(self, data):
	...

	tau = now() - tau

	if (orderType == E):
		if (BO):
			order_imbalance = e^(-p*tau) * order_imbalance + 1
		if (BB):
			order_imbalance = e^(-p*tau) * order_imbalance - 1

	...
