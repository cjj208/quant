# -*- coding: utf-8 -*-
import talib
import pandas as pd


tradedata = {
'SettlementPrice': "本次结算价",
'AskVolume3':"申卖量三",
'LowerLimitPrice': "跌停板价",
'UpdateMillisec': "最后修改毫秒",
'UpdateTime': '最后修改时间',
'ExchangeInstID': '合约在交易所的代码',
'ExchangeID': '交易所代码',
'CurrDelta': "今虚实度",
'AveragePrice': "均价乘合约乘数",
'AskPrice4': "申卖价四",
'PreOpenInterest': "昨持仓量",
'TradingDay': '交易日',
'BidVolume3': "申买量三",
'PreDelta': "昨虚实度",
'Volume': "成交量",
'PreClosePrice': "昨收盘",
'UpperLimitPrice': "涨停板价",
'AskVolume1': "申卖量一",
'BidPrice5': "申买价五",
'BidPrice4': "申买价四",
'AskPrice5': "申卖价五",
'BidVolume4': "申买量四",
'ClosePrice': "今收盘",
'AskVolume5':"申卖量五",
'BidPrice3': "申买价三",
'BidPrice2': "申买价二",
'ActionDay': "ActionDay",
'LastPrice': "最新价",
'LowestPrice': "最低价",
'AskPrice1': "申卖价一",
'AskVolume4': "申卖量四",
'AskVolume2': "申卖量二",
'HighestPrice': "最高价",
'BidPrice1': "申买价一",
'OpenPrice': "今开盘",
'InstrumentID': "合约代码",
'BidVolume2': "申买量二",
'OpenInterest': "持仓量",
'Turnover': "成交金额",
'AskPrice3': "申卖价三",
'AskPrice2': "申卖价二",
'BidVolume1': "申买量一",
'BidVolume5': "申买量五",
'PreSettlementPrice': "上次结算价"}

QryInvestorPosition = {
	'SettlementPrice':"本次结算价",
	'PositionDate': '持仓日期',
	'AbandonFrozen': "AbandonFrozen",
	'FrozenMargin':"冻结的保证金",
	'CloseProfitByDate':"逐日盯市平仓盈亏",
	'StrikeFrozen':"StrikeFrozen",
	'MarginRateByVolume':"保证金率(按手数)",
	'BrokerID':"经纪公司代码",
	'OpenCost':"开仓成本",
	'TodayPosition': "今日持仓",
	'OpenAmount': "开仓金额",
	'PosiDirection': "持仓多空方向",
	'YdPosition':"上日持仓",
	'FrozenCash': "冻结的资金",
	'ShortFrozen': "空头冻结",
	'CloseProfit': "平仓盈亏",
	'ShortFrozenAmount':"开仓冻结金额",
	'OpenVolume': "开仓量",
	'TradingDay':"交易日",
	'CloseVolume':"平仓量",
	'StrikeFrozenAmount':"冻结量",
	'InstrumentID':"合约代码",
	'CashIn': "资金差额",
	'HedgeFlag': "投机套保标志",
	'Commission': "手续费",
	'CloseAmount': "平仓金额",
	'UseMargin': "占用的保证金",
	'PositionProfit': "持仓盈亏",
	'InvestorID': "投资者代码",
	'LongFrozen': "多头冻结",
	'CombPosition': "组合成交形成的持仓",
	'PositionCost': "持仓成本",
	'MarginRateByMoney': "保证金率",
	'FrozenCommission': "冻结的手续费",
	'Position': "持仓量",
	'CombShortFrozen': "组合空头冻结",
	'CloseProfitByTrade': "逐笔对冲平仓盈亏",
	'PreMargin': "上次占用的保证金",
	'SettlementID': "结算编号",
	'ExchangeMargin': "交易所保证金",
	'LongFrozenAmount':"开仓冻结金额",
	'CombLongFrozen': "组合多头冻结",
	'PreSettlementPrice': "上次结算价",
}
Pattern = {
    '两只乌鸦':talib.CDL2CROWS,
    '三只乌鸦':talib.CDL3INSIDE,
    '三线打击':talib.CDL3LINESTRIKE,
    '三外部上涨和下跌':talib.CDL3OUTSIDE,
    '南方三星':talib.CDL3STARSINSOUTH,
    '三个白兵':talib.CDL3WHITESOLDIERS,
    '弃婴':talib.CDLABANDONEDBABY,
    '大敌当前':talib.CDLADVANCEBLOCK,
    '捉腰带线':talib.CDLBELTHOLD,
    '脱离':talib.CDLBREAKAWAY,
    '收盘缺影线中继线':talib.CDLCLOSINGMARUBOZU,
    '藏婴吞没':talib.CDLCONCEALBABYSWALL,
    '反击线':talib.CDLCOUNTERATTACK,
    '乌云压顶':talib.CDLDARKCLOUDCOVER,
    '十字':talib.CDLDOJI,
    '十字星':talib.CDLDOJISTAR,
    '蜻蜓十字/T形十字':talib.CDLDRAGONFLYDOJI,
    '吞噬模式':talib.CDLENGULFING,
    '十字暮星':talib.CDLEVENINGDOJISTAR,
    '暮星':talib.CDLEVENINGSTAR,
    '向上/下跳空并列阳线':talib.CDLGAPSIDESIDEWHITE,
    '墓碑十字/倒T十字':talib.CDLGRAVESTONEDOJI,
    '锤头':talib.CDLHAMMER,
    '上吊线':talib.CDLHANGINGMAN,
    '母子线':talib.CDLHARAMI,
    '十字孕线':talib.CDLHARAMICROSS,
    '风高浪大线':talib.CDLHIGHWAVE,
    '陷阱':talib.CDLHIKKAKE,
    '修正陷阱':talib.CDLHIKKAKEMOD,
    '家鸽':talib.CDLHOMINGPIGEON,
    '三胞胎乌鸦':talib.CDLIDENTICAL3CROWS,
    '颈内线':talib.CDLINNECK,
    '倒锤头':talib.CDLINVERTEDHAMMER,
    '反冲形态':talib.CDLKICKING,
    '由较长缺影线决定的反冲形态':talib.CDLKICKINGBYLENGTH,
    '梯底':talib.CDLLADDERBOTTOM,
    '长脚十字':talib.CDLLONGLEGGEDDOJI,
    '长蜡烛':talib.CDLLONGLINE,
    '光头光脚缺影线':talib.CDLMARUBOZU,
    '相同低价':talib.CDLMATCHINGLOW,
    '铺垫':talib.CDLMATHOLD,
    '十字晨星':talib.CDLMORNINGDOJISTAR,
    '晨星':talib.CDLMORNINGSTAR,
    '颈上线:中继':talib.CDLONNECK,
    '刺透形态':talib.CDLPIERCING,
    '黄包车夫':talib.CDLRICKSHAWMAN,
    '上升/下降三法':talib.CDLRISEFALL3METHODS,
    '分离线':talib.CDLSEPARATINGLINES,
    '射击之星':talib.CDLSHOOTINGSTAR,
    '短蜡烛':talib.CDLSHORTLINE,
    '纺锤':talib.CDLSPINNINGTOP,
    '停顿形态':talib.CDLSTALLEDPATTERN,
    '条形三明治':talib.CDLSTICKSANDWICH,
    '探水杆锤子线':talib.CDLTAKURI,
    '跳空并列阴阳线':talib.CDLTASUKIGAP,
    '插入线':talib.CDLTHRUSTING,
    '三颗星':talib.CDLTRISTAR,
    '奇特三河床':talib.CDLUNIQUE3RIVER,
    '向上跳空的两只乌鸦':talib.CDLUPSIDEGAP2CROWS,
    '上升/下降跳空三法':talib.CDLXSIDEGAP3METHODS,}
localPattern = {
        'tunshi':talib.CDLENGULFING,
        'guantouguanjiao':talib.CDLMARUBOZU,
        }




def zigzag(s, pct=5):
    ut = 1 + pct / 100
    dt = 1 - pct / 100

    ld = s.index[0]
    lp = s.Close[ld]
    tr = None

    zzd, zzp = [ld], [lp]

    for ix, ch, cl in zip(s.index, s.High, s.Low):
        # No initial trend
        if tr is None:
            if ch / lp > ut:
                tr = 1
            elif cl / lp < dt:
                tr = -1
        # Trend is up
        elif tr == 1:
            # New high
            if ch > lp:
                ld, lp = ix, ch
            # Reversal
            elif cl / lp < dt:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = -1, ix, cl
        # Trend is down
        else:
            # New low
            if cl < lp:
                ld, lp = ix, cl
            # Reversal
            elif ch / lp > ut:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = 1, ix, ch
    # Extrapolate the current trend
    if zzd[-1] != s.index[-1]:
        zzd.append(s.index[-1])

        if tr is None:
            zzp.append(s.Close[zzd[-1]])
        elif tr == 1:
            zzp.append(s.High[zzd[-1]])
        else:
            zzp.append(s.Low[zzd[-1]])

    return pd.Series(zzp, index=zzd)



def action(df):
    action = [0]
    direction = [0]    
    for i in df.index:
        print (df.iloc[i])
        if action[-1] == 0:
            if  (df.iloc[i,df.columns.get_loc("cross520")]==1) & (df.iloc[i,df.columns.get_loc("ma89144")]==1):

                df.iloc[i,df.columns.get_loc('action')] ='openBuy'
                action.append(1)
                direction.append(1)
        
    
            if  (df.iloc[i,df.columns.get_loc("cross520")]==-1) & (df.iloc[i,df.columns.get_loc("ma89144")]==-1):
    
                df.iloc[i,df.columns.get_loc('action')] ='openSell'
                action.append(-1)
                direction.append(-1)
              
    
        elif (action[-1] == 1) & (direction[-1] == 1):

            if  df.iloc[i,df.columns.get_loc('cross520')] == -1:
                df.iloc[i,df.columns.get_loc('action')] ='closeSell'
                action.append(0)
                direction.append(0)
    
    
        elif (action[-1] == -1) & (direction[-1] == -1):

            if  df.iloc[i,df.columns.get_loc('cross520')] == 1:
                
                df.iloc[i,df.columns.get_loc('action')] ='closeBuy'
                action.append(0)
                direction.append(0)

    return df
    
    