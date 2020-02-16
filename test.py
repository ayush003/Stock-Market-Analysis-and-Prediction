plt.figure(figsize=(20,10))
house_data['Close'].plot(color='black')
moving_10 = house_data['Close'].rolling(10).mean()
moving_10 .plot(color='b')

moving_40 = house_data['Close'].rolling(40).mean()
moving_40.plot(color='orange')