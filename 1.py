# -*- coding: utf-8 -*-
import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.ticker as ticker
import technical_indicators 
import config
import scipy.stats as scs
import empyrical
import time
import pyfolio as pf
pat = {'光头光脚缺影线':talib.CDLMARUBOZU,'吞噬模式':talib.CDLENGULFING,}


path = (r"F:\jimcfile\py_financial\python_p\python_p\jimc\rb1810_m5.csv")

df = pd.read_csv(path,encoding='gbk')
df = df.rename(columns={"//时间":"Date","开盘价":"Open","最高价":"High","最低价":"Low","收盘价":"Close","成交量":"Volume","持仓量":"openInterest"})

#df = df.set_index(df["Date"])

df = df.iloc[-2000:]

print (df)