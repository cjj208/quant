# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 11:02:49 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.ticker as ticker
import pickle
import config


pat = {'光头光脚缺影线':talib.CDLMARUBOZU,'吞噬模式':talib.CDLENGULFING,}


path = (r"rb1810_m5.csv")

df = pd.read_csv(path,encoding='gbk')
df = df.rename(columns={"//时间":"Date","开盘价":"Open","最高价":"High","最低价":"Low","收盘价":"Close","成交量":"Volume","持仓量":"openInterest"})
#print (df)
df = df.set_index(df["Date"])

df = df.iloc[-500:]


#df = df.reset_index()



date_tickers=df.Date
fig,ax=plt.subplots(figsize=(1200/72,480/72),facecolor='#CCCCCC')
df['zigzag'] = config.zigzag(df,0.6)
df['zigzagreturns'] = df[df.zigzag.isnull()==False].zigzag - df[df.zigzag.isnull()==False].zigzag.shift(periods=1,axis=0)#算zigzag的回报

quotes = []
for i ,j in enumerate(df.values):
    quotes.append(tuple([i]+list(j[1:])))
    #print (i)
    #print (j)
print (quotes[-1:])

    
gmmaine  = [3,5,8,10,12,15,30,35,40,45,50,60]
for i in gmmaine:
    df['sma'+ str(i)] = (talib.EMA(df["Close"], i)).round(3)
def format_date(x,pos=None):
    if x<0 or x>len(date_tickers)-1:
        return 

    return date_tickers[int(x)]
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax.grid(True)
fig.autofmt_xdate()
fig.autofmt_xdate()

ax.plot(df['sma3'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma5'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma8'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma10'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma12'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma15'],color="0", linewidth=1, linestyle="-")

ax.plot(df['sma30'],color="b", linewidth=1, linestyle="-")
ax.plot(df['sma35'],color="b", linewidth=1, linestyle="-")
ax.plot(df['sma40'],color="b", linewidth=1, linestyle="-")
ax.plot(df['sma45'],color="b", linewidth=1, linestyle="-")
ax.plot(df['sma50'],color="b", linewidth=1, linestyle="-")
ax.plot(df['sma60'],color="b", linewidth=1, linestyle="-")


#    ax.plot(df['zigzag'],color="#339933", linewidth=1, linestyle="--")
ax.plot(df[df.zigzag.isnull()==False].zigzag.index.values,df[df.zigzag.isnull()==False].zigzag.values,linewidth=1, linestyle="--")
candlestick_ohlc(ax,quotes,colordown='#009900', colorup='#FF6600',width=0.5)
#    plt.axvline("2018/06/20 14:00")
#动态画收盘价的价格与线
plt.axhline(df.iloc[-1:].Close.values,linewidth=1, linestyle="-",color='gray')
plt.text(df[-1:].index.values[0],(df.loc[df[-1:].index,["Close"]].values + 10),df[-1:].Close.values[0],fontsize=10,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0.8, 0),))
#列出zigzagreturn的总和
plt.text(df[-1:].index.values[0],(df.loc[df[-1:].index,["Close"]].values - 60),np.abs(df.zigzagreturns).sum(),fontsize=20,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0, 0),))

#count = 0
#for i in config.localPattern:
#    df[i] = config.localPattern[str(i)](df["Open"],df["High"],df["Low"],df["Close"])
#    candleSign = list(df[df[i] != 0].index.values)
#    for j in candleSign:
#        plt.text(j,(df.loc[j,["High"]])+count,i,fontsize=6,verticalalignment="top",horizontalalignment="center")
#    count += 0.3

for zig in list(df[df['zigzagreturns'].isnull()==False].index.values):#画zigzag连接注释
    
    barcolor = df.loc[zig,["zigzag"]][0] if df.loc[zig,['Close']][0]<=df.loc[zig,['Open']][0] else df.loc[zig,["zigzag"]][0]
    plt.text(zig,barcolor,df.loc[zig,["zigzagreturns"]].values[0],fontsize=5,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0.8, 0.8),))





plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.show()


