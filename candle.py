import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('housingFin.csv',index_col=0)
print(data.shape)
print(data.head())

data = data.drop(['Adjustment Type','Adjustment Factor','Volume'],axis=1)
data.head()

window = [5,10,20,50,100,200,400,500]

for win in window:
    mean_i = data['Close'].rolling(win).mean()
    std_dev_i = (data['Close'].rolling(win).var())**0.5
    
    # plt.figure(figsize=(20,10))
    # plt.plot(data.index,data['Close'],color='black')
    # plt.plot(data.index,mean_i,color='blue')
    # plt.fill_between(data.index,mean_i+std_dev_i,mean_i-std_dev_i,color='orange',alpha=0.5)
    # plt.show()
    
    profit = 0
    upper_band = mean_i+std_dev_i
    lower_band = mean_i-std_dev_i

    buy_price = 0
    sell_price = 0

    buy = True
    first = True

    for index,x in enumerate(data['Close'][20:]):
        if first and x>upper_band[index-1]:
            first = False
            sell_price = x
            buy = True
            continue

        if first and x<lower_band[index-1]:
            first = False
            buy_price = x
            buy = False
            continue

        if not buy and x>upper_band[index-1]:
            profit += x-buy_price
            sell_price = x
            buy = True
        elif buy and x<lower_band[index-1]:
            profit += sell_price-x
            buy_price = x
            buy = False
        
    print(profit,win)