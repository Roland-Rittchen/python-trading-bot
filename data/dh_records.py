import data.dh as dh
import event
import pandas as pd
from datetime import datetime
from pathlib import Path
import queue
import time

class RecordData(object): #dh.DataHandler
    def __init__(self,env, pair, timeout=0, count=0): #queue,pair=['EUR_USD'], date_start='2019_01', date_end="2020_04", timeout=0, count=0):
        self.queue=env['queue']
        self.pair=pair
        
        self.date_start=env['timerange'][0]
        self.date_end=env['timerange'][1]
        self.i=0
        self.df=pd.DataFrame()
        months=["2019-01"]#,"2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12",
            #"2020-01","2020-02","2020-03","2020-04"]

        #include DAY in timerange!

        self.folder=Path('E:\\')
        self.fto=self.folder / 'Data' / 'Records'
        for m in months: 
            for d in range(32):
                d+=1
                if d <10:
                    strd='-0'+str(d)
                else:
                    strd='-'+str(d)
                self.f=pair.replace('_', '')+'-'+m+strd+".csv"
                self.fto = self.fto / self.f
                try:
                    self.df = pd.read_csv(self.fto, names=['Symbol', 'Date_Time', 'Bid', 'Ask'],index_col=1, parse_dates=True)
                except FileNotFoundError:
                    pass 

    def connect(self,t=0.5):
        for row in self.df.itertuples(index=True):
            self.dat={'time':str(row[0]),'bid':row[2], 'ask':row[3]}
            
            self.dftemp = pd.DataFrame({'time':self.dat['time'],'bid':self.dat['bid'],'ask':self.dat['ask']}, index=[0])
            self.df=self.df.append(self.dftemp, ignore_index=True)
            self.event=event.TickEvent(self.dftemp,self.pair)
            self.queue.put(self.event)
            #print('data put in queue')
            self.i+=1
            if self.i > 100:
                break
            time.sleep(t)

    def disconnect(self):
        pass


if __name__ == '__main__':
    pass
    
