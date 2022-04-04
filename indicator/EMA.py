from indicator.indicator import Indicator
import talib

class EMA(Indicator):
    def __init__(self):
        pass

    def calc(self, ns):     #, frame, periods
        self.ema=ns.EUR_USD
        
        '''
        self.df_bid = self.convdata(data, frame)
        if len(self.df_bid.index) < periods[0]:
            self.perd = len(self.df_bid.index)
        else:
            self.perd = periods
        self.multi = 2/(self.perd+1)
        self.ema = 0
        while self.perd > 0:
            self.ema = self.df_bid.Close[:-self.perd]*self.multi + self.ema*(1-self.multi)
            self.perd-=1
        return self.ema
        '''
        ns.EUR_USD_EMA=self.ema