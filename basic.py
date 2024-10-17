
#This library facilitates backtesting of trading strategies.
from backtesting import Backtest, Strategy

#Used to check for crossover conditions between two indicators (e.g., moving averages)
from backtesting.lib import crossover

#The SME is used as an indicator function, while GOOG is a test dataset
from backtesting.test import SMA #, GOOG

#Fetching the data
import yfinance as yf

data=yf.download('BTC-USD',period='5y')
#print(data)

#Class Inheritance: SmaCross inherits from Strategy
#n1 and n2 represents the periods for short and long term moving averages
class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    #Create an indicator. I means indicator
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)
    
    #Create entry and exit logic
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()



#Creating a backtest object
bt = Backtest(data, SmaCross,
              cash=60000, commission=.002,
              exclusive_orders=True)

#Running the backtest object we have created
output = bt.run()
bt.plot()
print(output)