import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bot
import sys
import time


start = time.time()
if len(sys.argv) < 2:
	print("Usage: python3 bot.py <csv_filename>")
	exit()

data = pd.read_csv(str(sys.argv[1]),index_col=0)
print(data.shape)

first = True
buy = True
profit = 0

for i in range(5,len(data['Close'])):
	data1 = data[:i-1]
	step_ans = bot.predict(data1)
	if first :
		if step_ans == 1:
			buy = True
			buy_price = data['Close'][i]
			first = False
		elif step_ans == -1:
			buy = False
			sell_price = data['Close'][i]
			first = False
		else:
			continue
	else:
		if not buy and step_ans == 1:
			profit += sell_price - data['Close'][i]
			buy = True
			buy_price = data['Close'][i]
		elif buy and step_ans == -1:
			profit = data['Close'][i] - buy_price
			buy = False
			sell_price = data['Close'][i]
		else:
			continue

print("Net Profit = ",profit)
print(time.time()-start)