from backtesting import Backtest, Strategy
import pandas_ta as ta
import time

def get_sma(closing_price,l):
    s=ta.sma(closing_price,l)
    return s

def get_atr(high,low,close,leng):
    atr=ta.atr(high,low,close,leng)
    return atr
class sma_strategy(Strategy):
    n1=15
    n2=50
    atr_length=20
    def init(self):
        self.sma1=self.I(get_sma,self.data.Close.s,self.n1)
        self.sma2=self.I(get_sma,self.data.Close.s,self.n2)
        self.atr=self.I(get_atr,self.data.High.s,self.data.Low.s,self.data.Close.s,self.atr_length)

    def next(self):

        if (self.sma1[-1]<self.sma2[-1]) & (self.sma1[-2]>self.sma2[-2]):
            if self.position.is_short:
                self.position.close()
            self.buy(sl=self.data.Close[-1]*0.90,tp=self.data.Close[-1]*1.20)
        elif (self.sma1[-1]>self.sma2[-1]) & (self.sma1[-2]<self.sma2[-2]):
            if self.position.is_long:
                self.position.close()
            # self.sell()




import yfinance as yf
data=yf.download('^NSEBANK',period='10y')
print(data)

sma1=get_sma(data['Close'],15)
print(sma1)

atr=get_atr(data['High'],data['Low'],data['Close'],15)
print(atr)

bt=Backtest(data=data,strategy=sma_strategy,cash=50000)
results=bt.run()
print(results['_trades'])
# print(results[''])
bt.plot()