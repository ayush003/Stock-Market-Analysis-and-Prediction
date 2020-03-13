import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bot
import sys

if len(sys.argv) < 2:
	print("Usage: python3 bot.py <csv_filename>")
	exit()

data = pd.read_csv(str(sys.argv[1]),index_col=0)
print(data.shape)

print(bot.predict(data))
