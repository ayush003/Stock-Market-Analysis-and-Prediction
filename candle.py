import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

moving_10_large = []
mom_large = []

def bul_eglf(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return ((C_1 > O_1) & (O_0 > C_0)) & ((O_0 >= C_1) & (O_1 >= C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))

def bear_eglf(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return (O_1 > C_1) & (C_0 > O_0) & (C_0 >= O_1) & (C_1 >= O_0) & ((C_0 - O_0) > (O_1 - C_1 ))

def bul_har(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return (O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))

def bear_har(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return (C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))

def eve_star(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return (C_2 > O_2) & (min(O_1, C_1) > C_2) & (O_0 < min(O_1, C_1)) & (C_0 < O_0 )  

def mor_star(lst_0,lst_1,lst_2):    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    return (C_2 < O_2) & (min(O_1, C_1) < C_2) & (O_0 > min(O_1, C_1)) & (C_0 > O_0 )

def bul_eglf_func(arr):
	bul_eglf_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if bul_eglf(lst_0,lst_1,lst_2) and moving_10_large[c]<moving_10_large[c-1]:
	        bul_eglf_arr.append(c)

	for x in bul_eglf_arr[::-1]:
	  count = 0
	  for y in range(x,min(x+15,len(moving_10_large))):
	    if mom_large[y]>0:
	      count+=1
	  if count>=5:
	    return x
	return -1

def bear_eglf_func(arr):
	bear_eglf_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if bear_eglf(lst_0,lst_1,lst_2) and moving_10_large[c]>moving_10_large[c-1]:
	        bear_eglf_arr.append(c)

	for x in bear_eglf_arr[::-1]:
	  count = 0
	  for y in range(x,min(x+20,len(moving_10_large))):
	    if mom_large[y]<0:
	      count+=1
	  if count>=5:
	    return x
	return -1

def bul_har_func(arr):
	bul_har_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if bul_har(lst_0,lst_1,lst_2) and moving_10_large[c]<moving_10_large[c-1]:
	        bul_har_arr.append(c)
	for x in bul_har_arr[::-1]:
		count = 0
		for y in range(x,min(x+15,len(moving_10_large))):
			if mom_large[y]>0:
				count+=1
			if count>=5:
				return x
	return -1

def bear_har_func(arr):
	bear_har_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if bear_har(lst_0,lst_1,lst_2) and moving_10_large[c]>moving_10_large[c-1]:
	        bear_har_arr.append(c)


	for x in bear_har_arr[::-1]:
		count = 0
		for y in range(x,min(x+20,len(moving_10_large))):
			if mom_large[y]<0:
			  count+=1
			if count>=5:
				return x
	return -1

def eve_star_func(arr):
	eve_star_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if eve_star(lst_0,lst_1,lst_2) and moving_10_large[c]>moving_10_large[c-1]:
	        eve_star_arr.append(c)

	for x in eve_star_arr:
		count = 0
		for y in range(x,min(x+20,len(moving_10_large))):
			if mom_large[y]<0:
				count+=1
			if count>=5:
				return x
	return -1

def mor_star_func(arr):
	mor_star_arr = []
	for c in range(2,len(arr['Close'])):
	    lst_2=[arr['Open'].iloc[c-2],arr['High'].iloc[c-2],arr['Low'].iloc[c-2],arr['Close'].iloc[c-2]]
	    lst_1=[arr['Open'].iloc[c-1],arr['High'].iloc[c-1],arr['Low'].iloc[c-1],arr['Close'].iloc[c-1]]
	    lst_0=[arr['Open'].iloc[c],arr['High'].iloc[c],arr['Low'].iloc[c],arr['Close'].iloc[c]]
	    if mor_star(lst_0,lst_1,lst_2) and moving_10_large[c]<moving_10_large[c-1]:
	        mor_star_arr.append(c)

	for x in mor_star_arr:
		count = 0
		for y in range(x,min(x+15,len(moving_10_large))):
			if mom_large[y]>0:
				count+=1
			if count>=5:
				return x
	return -1

def candle_pred(data):
	global moving_10_large
	global mom_large
	if len(data['Close'])>100: data = data[-100:]
	moving_10_large = data['Close'].rolling(10).mean()
	mom_large = np.gradient(moving_10_large)

	# print("Bullish Engulfing found at : ",bul_eglf_func(data))
	# print("Bearish Engulfing found at : ",bear_eglf_func(data))
	# print("Bullish Harami found at : ",bul_har_func(data))
	# print("Bearish Harami found at : ",bear_har_func(data))
	# print("Evening Star found at : ",eve_star_func(data))
	# print("Morning Star found at : ",mor_star_func(data))

	result_array = np.array([bul_eglf_func(data),bear_eglf_func(data),bul_har_func(data),bear_har_func(data),eve_star_func(data),mor_star_func(data)])
	res_index = np.argmax(result_array)
	
	if result_array.sum() == -6:
		return -1

	return (0 if (res_index&1) else 1)

