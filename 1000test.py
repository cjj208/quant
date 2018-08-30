# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 17:50:09 2018

@author: JimchanChen
"""

# -*- coding: utf-8 -*-
import numpy as np
import talib
import mpl_finance 
import pandas as pd
#import matplotlib.finance as mpf
import matplotlib.pyplot as plt
from matplotlib import style
from pyti.exponential_moving_average import exponential_moving_average as ema
import pyti
import Ta_Lib as tl


period = 10


path = (r"d:\XAUUSD_H4.csv")
path2 = (r'd:\XAUUSD_D1.csv')

row = ['Date','Time','Open','High','Low','Close','Volume']

df = pd.read_csv(path2,header=0,names=row,parse_dates=True,index_col=0)
#kline = df["Open"].values,df["High"].values,df["Low"].values,df["Close"].values
#由于tailib不能使用pandas的数据列，因此转换成VALUES
df['ma10'] = ema(df['Close'], period)
print (df.tail())

