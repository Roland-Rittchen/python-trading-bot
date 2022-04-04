#sample strat: buy on EMA signal, trailing SL
from strategy.strategy import Strategy

class Strat(Strategy):
    def __init__(self):
        self.indicators = [{'name':'EMA 26 Period','ind':'EMA','parameters':[26],'timeframe':'5m'}]

    def onTick(self):
        pass

    def onBar(self):
        pass