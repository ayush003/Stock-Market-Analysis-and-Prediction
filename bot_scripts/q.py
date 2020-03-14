import random
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
# data = data1ta[:300]

moving_10_large = data['Close'].rolling(10).mean()
mom_large = np.gradient(moving_10_large)

total_trades = 0
positive = 0

for i in range(5,len(data['Close'])-1):
	print(i)
	data1 = data[max(0,i-300):i-1]
	step_ans = bot.predict(data1)

	if step_ans == 0:
		continue
	if step_ans == 1:
		count = 0
		for y in range(i,min(i+15,len(moving_10_large))):
			if mom_large[y]>0:
				count+=1
			if count>=5:
				positive+=1
				break
	else:
		count = 0
		for y in range(i,min(i+15,len(moving_10_large))):
			if mom_large[y]<0:
				count+=1
			if count>=5:
				positive+=1
				break
	total_trades+=1

print("Accuracy = ",(positive*100)/total_trades)

print(time.time()-start)