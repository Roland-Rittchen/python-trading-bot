import pandas as pd

class Indicator(object):
    def __init__(self, data, frame, periods):
        self.data = data
        self.periods = periods

    def convdata(self, data, frame):
        self.dt=data.set_index('time')
        self.dt.index = pd.to_datetime(self.dt.index)
        self.df_bid =self.dt['bid'].resample(frame).ohlc()
        self.df_bid.columns = ['Open', 'High', 'Low', 'Close']
        self.df_bid.index.name = "Date"
        return self.df_bid