#indicator handler, handling all separate indicators and collecting their signals
from dataclasses import dataclass
import pandas as pd
from indicator.EMA import EMA
from indicator.MACD import MACD
from indicator.trend import Trend
import time

@dataclass
class IndicatorList:
    EMA: bool = True
    MACD: bool = False
    Trend: bool = False

class IndicatorHandler(object):
    
    def __init__(self, env):
        self.indicators=[]
        for i in env.indicators:
            self.addInst(i)

    def addInst(self, indicator):
        self.indicators.append(EMA())

    def start(self, ns):
        while True:
            for i in self.indicators:
                i.calc(ns)
            time.sleep(5)    

    '''
    def calcIndicators(self, Indicatorlist, data, frame, periods):
        if Indicatorlist.EMA:
            self.hEMA = EMA.calc(self, data, frame, periods)
        if Indicatorlist.MACD:
            self.hMACD = MACD.calc(self, data, frame, periods)
        dftemp = pd.DataFrame({'time':data['time'],'EMA':self.hEMA,'MACDfast':self.hMACD[0],'MACDslow':self.hMACD[1]}, index=[0])
        try:
            dfi
        except NameError:
            dfi = None

        if dfi is None:
            dfi = pd.DataFrame(columns=['time','EMA','MACDfast','MACDslow'])
        else:
            dfi=dfi.append(dftemp, ignore_index=True)
    '''