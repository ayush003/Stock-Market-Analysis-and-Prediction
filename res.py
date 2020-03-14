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
data = data[:300]


total_trades = 0
positive = 0

# trade_ar = []
# dec_array = []
# color_ar = ['red','white','green']
for i in range(5,len(data['Close'])-1):
	print(i)
	data1 = data[max(0,i-300):i-1]
	step_ans = bot.predict(data1)
	# step_ans = random.randint(-1,1)
	# dec_array.append(color_ar[step_ans+1])
	if step_ans == 0:
		continue
	if (step_ans == 1 and data['Close'][i+1]>data['Close'][i]) \
		or (step_ans == -1 and data['Close'][i+1]<data['Close'][i]):
		positive+=1
	total_trades+=1

print("Accuracy = ",(positive*100)/total_trades)

# plt.plot(data.index,data['Close'],color='black')
# plt.scatter(data.index[5:],data['Close'][5:],color = dec_array)
# plt.scatter(data.index[trade_ar],data['Close'][trade_ar],color=dec_array)
# plt.show()


# print("Net Profit = ",profit)
print(time.time()-start)