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
import technical_indicators 
import config
import scipy.stats as scs
import empyrical
import time
import pyfolio as pf
pat = {'光头光脚缺影线':talib.CDLMARUBOZU,'吞噬模式':talib.CDLENGULFING,}


path = (r"rb1810_m5.csv")

df = pd.read_csv(path,encoding='gbk')
df = df.rename(columns={"//时间":"Date","开盘价":"Open","最高价":"High","最低价":"Low","收盘价":"Close","成交量":"Volume","持仓量":"openInterest"})

#df = df.set_index(df["Date"])

df = df.iloc[-2000:]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#重新生成转换K线数据
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


date_tickers=df.Date.values
weekday_quotes=[tuple([i]+list(quote[1:])) for i,quote in enumerate(df.values)]
df = df.reset_index()
df['limt'] =np.nan
def limt(df):
    i = 0
    count = 0
    LIM = []
    
    
    for i in df.index:
        # df.iloc[-1,df.columns.get_indexer(['High'])].values[0]>df.iloc[-1-i,df.columns.get_indexer(['High'])].values[0]:
        if df.High.shift(i).values[-1]>df.iloc[-1,df.columns.get_indexer(['High'])].values[0]:
            count+=1
            if count ==3:
                print (count)
                df.iloc[-1,df.columns.get_indexer(['limt'])] = df.High.shift(1).values[-i]
                LIM.append(df.iloc[-1,df.columns.get_indexer(['High'])].values[0])
        i+=1

    return LIM[0]




#limt(df)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#将指标添加进来
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


avgline = [5,10,20,89,144,]
for i in avgline:
    df['sma'+ str(i)] = df.Close.rolling(i).mean()
#收盘价小于89并且大于144或收盘价小于144大于89，标注为0，不作任何操作，收盘价大于144，并且大于89，为1，否则为-1
df['ma89144']=np.where(((df.Close>df.sma144)&(df.Close<df.sma89))|((df.Close<df.sma144)&(df.Close>df.sma89)),0,np.where(((df.Close>df.sma144)&(df.Close>df.sma89)),1,-1))
df['cross520']=np.where((df.Close>df.sma5)&((df.sma5>df.sma10)&(df.sma10>df.sma20)),1,np.where((df.Close<df.sma5)&((df.sma5<df.sma10)&(df.sma10<df.sma20)),-1,0))
df['closlimt'] = np.where((df.Close>df.sma5)&(df.Close>df.sma10),1,np.where((df.Close<df.sma5)&(df.Close<df.sma10),-1,0))
#df = technical_indicators.donchian_channel(df,10)
df = technical_indicators.average_true_range(df,10)
df = technical_indicators.donchian_channel(df,5)

#df['limtup'] = df.Close-df.Donchian_14
#df['limtdown'] = df.Close+df.Donchian_14

#---------------------------------------------------------------------
#回测函数
#---------------------------------------------------------------------
#def action(df):

df['action'] =np.nan
df['actionreturn'] =np.nan

action = [0]
direction = [0]   
actionindex = [] #开仓时的行号
for i in df.index[200:]:
    count = 0
#    print (df[:i])
    if df.High.shift(i).values[-1]>df.iloc[-1,df.columns.get_indexer(['High'])].values[0]:
        count+=1
        if count ==3:
            df.iloc[-1,df.columns.get_indexer(['limt'])] = df.High.shift(1).values[-i]

    if action[-1] == 0:
        if  (df.iloc[i,df.columns.get_loc("cross520")]==1) & (df.iloc[i,df.columns.get_loc("ma89144")]==1):
            df.iloc[i,df.columns.get_loc('action')] ='OB'
            action.append(1)
            direction.append(1)
            actionindex.append(i)
       

        if  (df.iloc[i,df.columns.get_loc("cross520")]==-1) & (df.iloc[i,df.columns.get_loc("ma89144")]==-1):

            df.iloc[i,df.columns.get_loc('action')] ='OS'
            action.append(-1)
            actionindex.append(i)
            direction.append(-1)
    


    elif (action[-1] == 1) & (direction[-1] == 1):
        if  df.iloc[i,df.columns.get_loc('cross520')] == -1:
            df.iloc[i,df.columns.get_loc('action')] ='CS'
            df.iloc[i,df.columns.get_loc('actionreturn')] =df.iloc[i,df.columns.get_loc('Close')]-df.iloc[actionindex[-1],df.columns.get_loc('Close')]
        
            action.append(0)
            direction.append(0)


    elif (action[-1] == -1) & (direction[-1] == -1):

        if  df.iloc[i,df.columns.get_loc('cross520')] == 1:
            
#        if  df.iloc[i,df.columns.get_loc('Close')] <limt(df):
            df.iloc[i,df.columns.get_loc('action')] ='CB'
            action.append(0)
            direction.append(0)
            df.iloc[i,df.columns.get_loc('actionreturn')] =df.iloc[actionindex[-1],df.columns.get_loc('Close')] - df.iloc[i,df.columns.get_loc('Close')]
            


df['actionreturn_cumsum'] = df[df.actionreturn.isnull()==False].actionreturn.cumsum()#总收益
#---------------------------------------------------------------------
#策略结果
#---------------------------------------------------------------------
action = df[df.action.isnull()==False]#所有买卖行动状态 
action = action.reset_index()
action = action[['Date','action','actionreturn','actionreturn_cumsum',]]
action['Date'] = pd.to_datetime(action['Date'],format="%Y-%m-%d %H:%M")
action = action.set_index('Date')


action['returns_rate'] = (action['actionreturn']*10)/20000 #十倍杠杆加投入五万的收益率
#action['returnsD'] = action['returns'].resample('D',label='left',).sum()

action['returns_cum_returns'] = empyrical.cum_returns(action['returns_rate'])#计算累计收益


print ("开始时间:\t",str(action.index[0]))
print ("结束时间:\t",str(action.index[-1]))
print ("总收益:\t¥{0}:"  .format(action.actionreturn_cumsum[-1]*10))
print ("总收益率:\t{0:.3}%:"  .format(action.returns_cum_returns[-1]*100))
print ("做多次数:\t",action[action.action.isin(["OB"])==True].action.count())
print ("做空次数:\t",action[action.action.isin(["OS"])==True].action.count())
print ('年化收益:\t%.3f:' % (empyrical.annual_return(action['returns_rate'])))
print ('夏普比率:\t%.3f:' % (empyrical.sharpe_ratio(action['returns_rate'],)))
print ('最大回撤:\t%.3f:' % (empyrical.max_drawdown(action['returns_rate'],)))

action.to_csv('action.csv')
#---------------------------------------------------------------------




fig,ax=plt.subplots(figsize=(1200/72,480/72),facecolor='#CCCCCC',edgecolor='black')
plt.subplots_adjust(top=0.970,bottom=0.137,left=0.031, right=0.958,hspace=0.2,wspace=0.2)
ax.set_facecolor('#CCCCCC')
ax.plot(df['sma5'],color="gray", linewidth=1, linestyle="-")
ax.plot(df['sma10'],color="gray", linewidth=1, linestyle="-")
ax.plot(df['sma20'],color="gray", linewidth=1, linestyle="-")
ax.plot(df['sma89'],color="0", linewidth=1, linestyle="-")
ax.plot(df['sma144'],color="0", linewidth=1, linestyle="-")

#ax.plot(df['donchian_low_20'],color="0", linewidth=1, linestyle="-")

ax.fill_between(df.index,df['sma144'],df['sma89'],color='#ADCCFF', alpha='0.4')
ax.fill_between(df.index,df['sma5'],df['sma20'],color='darkorange', alpha='0.4')

#ax1 = plt.subplot(2,1,2)

candlestick_ohlc(ax,weekday_quotes,colordown='0', colorup='darkorange',width=0.5)


#---------------------------------------------------------------------
#动态画收盘价的价格与线
#plt.axhline(df.iloc[-1:].Close.values,linewidth=1, linestyle="-",color='gray')
#plt.text(df[-1:].index.values[0],(df.loc[df[-1:].index,["Close"]].values + 10),df[-1:].Close.values[0],fontsize=10,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0.8, 0),))
#---------------------------------------------------------------------
#计算zigzag与总返回的值并标注在图
#---------------------------------------------------------------------
#df['zigzag'] = config.zigzag(df,0.6)
#df['zigzagreturns'] = df[df.zigzag.isnull()==False].zigzag - df[df.zigzag.isnull()==False].zigzag.shift(periods=1,axis=0)#算zigzag的回报
#plt.text(df[-1:].index.values[0],(df.loc[df[-1:].index,["Close"]].values - 60),np.abs(df.zigzagreturns).sum(),fontsize=20,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0, 0),))
#for zig in list(df[df['zigzagreturns'].isnull()==False].index.values):#画zigzag连接注释
#    
#    barcolor = df.loc[zig,["zigzag"]][0] if df.loc[zig,['Close']][0]<=df.loc[zig,['Open']][0] else df.loc[zig,["zigzag"]][0]
#    plt.text(zig,barcolor,df.loc[zig,["zigzagreturns"]].values[0],fontsize=5,verticalalignment="top",horizontalalignment="center",bbox=dict(boxstyle="round",alpha=0.8,ec=(0, 0, 0),fc=(1., 0.8, 0.8),))

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#K线形态标注     
#---------------------------------------------------------------------
#count = 0
#for i in config.localPattern:
#    df[i] = config.localPattern[str(i)](df["Open"],df["High"],df["Low"],df["Close"])
#    candleSign = list(df[df[i] != 0].index.values)
#    for j in candleSign:
#        plt.text(j,(df.loc[j,["High"]])+count,i,fontsize=6,verticalalignment="top",horizontalalignment="center")
#    count += 0.3
#    









#---------------------------------------------------------------------
for i in list(df[df['action'].isnull()==False].index.values):
    
    barcolor = df.loc[i,["High"]][0] if df.loc[i,['Close']][0]<=df.loc[i,['Open']][0] else df.loc[i,["Low"]][0]
    if  df.loc[i,['action']][0] == 'OB':
        plt.annotate(df.loc[i,["action"]].values[0], xy=(i, df.loc[i,["Close"]][0]),
                 arrowprops=dict(facecolor='r', shrink=0.05,width=1,headwidth=8,headlength=8))
    elif df.loc[i,['action']][0] == 'OS':
        plt.annotate(df.loc[i,["action"]].values[0], xy=(i, df.loc[i,["Close"]][0]),rotation=15,
                 arrowprops=dict(facecolor='g', shrink=0.05,width=1,headwidth=8,headlength=8))
        
    else:
        plt.annotate(df.loc[i,["action"]].values[0], xy=(i, df.loc[i,["Close"]][0]),rotation=15,
                 arrowprops=dict(facecolor='yellow', shrink=0.05,width=1,headwidth=8,headlength=8))
        
        
        
def format_date(x,pos=None):
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]
#---------------------------------------------------------------------
#回测返回参数
#---------------------------------------------------------------------
plt.text(100,4500,("盈亏：%s"%(action.actionreturn.sum())),fontsize=20,verticalalignment="top",
             horizontalalignment="center",color='gray')


ax1 = ax.twinx()
ax1.set_ylim(-200, 200)
ax1.plot(df[df.actionreturn_cumsum.isnull()==False].actionreturn_cumsum.index.values,
            df[df.actionreturn_cumsum.isnull()==False].actionreturn_cumsum.values,linewidth=1, linestyle="--")
ax1.fill_between(df.index,df['actionreturn_cumsum'],0,color='0', alpha='0.8')
ax1.axhline(0,linewidth=1, linestyle="-",color='0')
for i in list(df[df['actionreturn'].isnull()==False].index.values):
    plt.text(i-1,df.loc[i,["actionreturn_cumsum"]][0],df.loc[i,["actionreturn"]].values[0],fontsize=10,verticalalignment="top",
             horizontalalignment="center",color='gray')

ax1.plot(df['ATR_10'],color="0", linewidth=1, linestyle="-")
ax1.plot(df['Donchian_5'],color="0", linewidth=1, linestyle="-")
#ax1.bar(df.actionreturn)
#---------------------------------------------------------------------
# 正态分布图   
#---------------------------------------------------------------------
ax2 = fig.add_subplot(339) 
ax2.set_facecolor('#CCCCCC')
ax2.xaxis.set_ticks_position('top')
actionreturn = df['actionreturn'].dropna()

# 均值期望
stock_mean = actionreturn.mean()
# 标准差
stock_std = actionreturn.std()


# 绘制股票0的直方图
plt.hist(actionreturn, bins=100, density=True,)
# linspace从股票0 最小值－> 最大值生成数据
fit_linspace = np.linspace(actionreturn.min(),actionreturn.max(),num=50)

# 概率密度函数(PDF，probability density function)
# 由均值，方差，来描述曲线，使用scipy.stats.norm.pdf生成拟合曲线
pdf = scs.norm(stock_mean, stock_std).pdf(fit_linspace)
cdf = scs.cumfreq(actionreturn)
# plot x, y
plt.plot(fit_linspace, pdf,lw=2, c='r')

plt.show()
#print (df.describe())

    
    
#---------------------------------------------------------------------   
#plt.fill(ax1, facecolor='purple',interpolate=True)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax.grid(True)
fig.autofmt_xdate()
df.to_csv('quant.csv')
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.show()
