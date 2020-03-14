import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import candle


def ma(arr,win):
	if (win<0 or 4*win>len(arr['Close'])):
		return 0,0,0
	moving_i = arr['Close'].rolling(win).mean()
	moving_4i = arr['Close'].rolling(4*win).mean()
	moving_4i = moving_4i.dropna()
	moving_i = moving_i.iloc[len(moving_i)-len(moving_4i):]
	close_i = arr['Close']
	close_i = close_i.iloc[len(close_i)-len(moving_4i):]

	my_color_i = np.where(moving_i>moving_4i,'g','r')
	price_diff_i = (moving_i - moving_4i)
	zero_crossings_i = np.where(np.diff(np.sign(price_diff_i)))[0]
	zero_crossings_i+=1

	buy_i = 0
	sell_i = 0

	net_profit_i = 0
	if len(zero_crossings_i)>0:
	    if my_color_i[zero_crossings_i[0]] == 'r':
	        sell_i = close_i[zero_crossings_i[0]]
	    else :
	        buy_i = close_i[zero_crossings_i[0]]

	    for j in zero_crossings_i[1:]:
	        if my_color_i[j] == 'r':
	            net_profit_i += close_i[j] - buy_i
	            sell_i = close_i[j]
	        else : 
	            net_profit_i+=sell_i-close_i[j]
	            buy_i = close_i[j]

	num_true = 0
	num_false = 0
	if len(zero_crossings_i)>0:
	    for k,j in enumerate(my_color_i[:-1]):
	        if j=='r':
	            if close_i[k+1]>=close_i[k]:
	                num_true+=1
	            else:
	                num_false+=1
	        else:
	            if close_i[k+1]<=close_i[k]:
	                num_true+=1
	            else:
	                num_false+=1

		# return net_profit_i, ((num_true/(num_true+num_false))*100)
	#returning the net profit, accuracy and the buy = 1 /sell = 0 decision
	# return net_profit_i,0,((1 if moving_i[-1]>moving_4i[-1] else -1) if len(arr['Close']) in zero_crossings_i else 0)
	return net_profit_i,0,(1 if moving_i[-1]>moving_4i[-1] else -1)

def snr(arr,win):
	if len(arr['Close'])<4 : return float('-inf'),0	
	from findiff import FinDiff #pip3 install findiff
	dx = 1 #1 day interval
	d_dx = FinDiff(0, dx, 1)
	d2_dx2 = FinDiff(0, dx, 2)
	clarr = np.asarray(arr['Close']).astype(float)
	mom = d_dx(clarr)
	momacc = d2_dx2(clarr)

	def get_extrema(isMin):
	  return [x for x in range(len(mom))
	    if (momacc[x] > 0 if isMin else momacc[x] < 0) and
	      (mom[x] == 0 or #slope is 0
	        (x != len(mom) - 1 and #check next day
	          (mom[x] > 0 and mom[x+1] < 0 and
	           arr['Close'][x] >= arr['Close'][x+1] or
	           mom[x] < 0 and mom[x+1] > 0 and
	           arr['Close'][x] <= arr['Close'][x+1]) or
	         x != 0 and #previous day
	          (mom[x-1] > 0 and mom[x] < 0 and
	           arr['Close'][x-1] < arr['Close'][x] or
	           mom[x-1] < 0 and mom[x] > 0 and
	           arr['Close'][x-1] > arr['Close'][x])))]
	minimaIdxs, maximaIdxs = get_extrema(True), get_extrema(False)

	profit = 0
	buy_price = 0
	sell_price = 0  
	resist = False
	first = True
	buy = True

	resistance_plot_array = []
	support_plot_array = []
	trade_dec = 0	#1 for buy, -1 for sell, 0 for hold

	for end_index in range(win,len(clarr)):
		price_max = clarr[end_index-win:end_index].max()
		price_min = clarr[end_index-win:end_index].min()
		delta_5 = (price_max - price_min)*0.05

		max_num = 0
		resistance_centre_recent = -1
		for x in maximaIdxs:
		  if x<end_index-win:
		    continue
		  if x>=end_index:
		    break

		  num_points = 0
		  for y in maximaIdxs:
		    if y<end_index-win:
		      continue			
		    if y>=end_index:
		      break
		    if (clarr[x] >= clarr[y]) and (clarr[x] - clarr[y])<=delta_5:
		        num_points+=y*clarr[y]
		  if num_points>max_num:
		      max_num = num_points
		      resistance_centre_recent = x

		min_num = 1
		support_centre_recent = -1
		for x in minimaIdxs:
		  if x<end_index-win:
		    continue
		  if x>=end_index:
		    break
		  num_points = 0
		  for y in minimaIdxs:
		    if y<end_index-win:
		      continue
		    if y>=end_index:
		      break
		    if clarr[y]>clarr[x] and clarr[y]-clarr[x]<=delta_5:
		        num_points-=y*(price_max-clarr[y])
		  if num_points<min_num:
		      min_num = num_points
		      support_centre_recent = x

		resistance_price = clarr[resistance_centre_recent] if resistance_centre_recent!=-1 else price_max
		support_price = clarr[support_centre_recent] if support_centre_recent!=-1 else price_min
		resistance_plot_array.append(resistance_price)
		support_plot_array.append(support_price)

		x = clarr[end_index]
		if abs(x-resistance_price) <= abs(x-support_price):
		    resist = True
		else:
		    resist = False

		if first:
		    if (resist and (x>=resistance_price or resistance_price - x <= delta_5)) :
		        trade_dec = -1
		        sell_price = x
		        buy = False
		        first = False
		    if not resist and (x<=support_price or x-support_price <= delta_5):
		        trade_dec = 1
		        buy = True
		        buy_price = x
		        first = False
		    continue
		    
		if buy and resist and (x>=resistance_price or resistance_price - x <= delta_5):
		    trade_dec = -1
		    profit += x - buy_price
		    buy = False
		    sell_price = x
		    
		if not buy and not resist and (x<=support_price or x-support_price <= delta_5):
		    trade_dec = 1
		    profit += sell_price - x 
		    buy = True
		    buy_price = x
	      
	return profit,trade_dec

def bollinger(arr,win):
	mean_i = arr['Close'].rolling(win).mean()
	std_dev_i = (arr['Close'].rolling(win).var())**0.5
	profit = 0
	upper_band = mean_i+std_dev_i
	lower_band = mean_i-std_dev_i

	buy_price = 0
	sell_price = 0

	buy = True
	first = True
	trade_dec = 0	#1 for buy, -1 for sell, 0 for hold

	for index,x in enumerate(arr['Close'][20:]):
	    if first and x>upper_band[index-1]:
	        first = False
	        trade_dec = -1
	        sell_price = x
	        buy = True
	        continue

	    if first and x<lower_band[index-1]:
	    	trade_dec = 1
	    	first = False
	    	buy_price = x
	    	buy = False
	    	continue

	    if not buy and x>upper_band[index-1]:
	    	trade_dec = -1
	    	profit += x-buy_price
	    	sell_price = x
	    	buy = True
	    elif buy and x<lower_band[index-1]:
	    	trade_dec = 1
	    	profit += sell_price-x
	    	buy_price = x
	    	buy = False
	    
	return profit,trade_dec

def predict(data):
	window = [1,5,10,20,50,100]

	print("Moving Average:")
	max_profit_win_ma = -1
	max_prof_ma = -1000000000
	for i in window:
		temp,_,t1 = ma(data,i)
		if t1 == 0:
			continue
		if temp>max_prof_ma:
			max_profit_win_ma = i
			max_prof_ma = temp
	print("Profit = ",max_prof_ma," Window = ",max_profit_win_ma)

	print()
	print("Bollinger Bands:")
	max_profit_win_bol = -1
	max_prof_bol = -1000000000
	for i in window:
		temp,_ = bollinger(data,i)
		if temp>max_prof_bol:
			max_profit_win_bol = i
			max_prof_bol = temp
	print("Profit = ",max_prof_bol," Window = ",max_profit_win_bol)
	print()

	print("Support and Resistance:")
	max_profit_win_snr = -1
	max_prof_snr = -1000000000
	for i in window:
		temp,_ = snr(data,i)
		if temp>max_prof_snr:
			max_profit_win_snr = i
			max_prof_snr = temp
	print("Profit = ",max_prof_snr," Window = ",max_profit_win_snr)

	pred_final = []
	_,_,temp = ma(data,max_profit_win_ma)
	pred_final.append(temp)

	_,temp = bollinger(data,max_profit_win_bol)
	pred_final.append(temp)

	_,temp = snr(data,max_profit_win_snr)
	pred_final.append(temp)

	temp = candle.candle_pred(data)
	pred_final.append(temp)

	print()
	if(pred_final[-1]==0):
		print("No pattern")
	else:
		print("Latest pattern shows ",("Bullish" if pred_final[-1]==1 else "Bearish")," trend.")

	print(pred_final)
	pred_final[0]/=10
	pred_final[1]*=0.3
	pred_final[2]*=0.2
	pred_final[3]*=0.4
	return_pred = sum(pred_final)
	if return_pred > 0:
		return 1
	elif return_pred < 0:
		return -1
	else:
		return 0
