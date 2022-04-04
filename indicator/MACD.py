from indicator.indicator import Indicator
from indicator.EMA import EMA

class MACD(Indicator):
    def calc(self, data, frame, periods):
        self.fast = [periods[1]]
        self.slow = [periods[2]]
        return [EMA.calc(self,data, frame, self.fast), EMA.calc(self,data, frame, self.slow)]