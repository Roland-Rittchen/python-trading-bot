#import data.dh as dh
import event
import pandas as pd
from datetime import datetime
from pathlib import Path
from multiprocessing import Queue
import time
import csv
import platform
import os
import operator

class TrueFXData(object): #dh.DataHandler
    def __init__(self, pairs, dQ, date_start='2019_01', date_end="2020_04", timeout=0, count=0): #queue,pair=['EUR_USD'], date_start='2019_01', date_end="2020_04", timeout=0, count=0):
        self.queue=dQ
        self.pairs=pairs
        self.connected = True
        
        self.date_start=date_start
        self.date_end= date_end

        self.i=0
        self.tList=[] #list for readout
        
        # TO DO - IMPLEMENT ACTUAL WORKING START AND END DATES!
        self.months=["2019-01"]#,"2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12",
            #"2020-01","2020-02","2020-03","2020-04"]
        self.folder=Path('E:\\')
        self.fto=self.folder / 'Data' / 'TrueFX_raw'
        
        if platform.system() == 'Windows':
            self.src_dir =os.path.join('E:\\','Data','TrueFX_raw')

        for m in self.months:
            #read out data from all pairs
            for p in self.pairs: 
                self.f=p.replace('_', '')+'-'+m+".csv" #filename
                self.fto = os.path.join(self.src_dir,self.f) #file to open

                with open(self.fto, "r") as fo:
                    reader = csv.reader(fo, delimiter="\t")
                    rownum = 1
                    for row in reader:
                        if rownum == 0:
                            #header = row  #work with header row if you like
                            pass
                        else:
                            self.tList.append(row[0].split(",")) 
                            #print(row[0].split(","))
                        rownum += 1
                        if rownum > 100000: #limit run for test purpose
                            break
        self.tList.sort(key=lambda x: x[1])

        #for l in self.tList:
        #    print(l)



    def connect(self, t=0.0001):
        self.connected = True
        while self.connected:
            if len(self.tList) > 0:
                self.dat=self.tList.pop(0)
                self.queue.put(event.TickEvent([self.dat[1],self.dat[2],self.dat[3],0], self.dat[0].replace('/', '_')))
                #self.dftemp = pd.DataFrame({'time':self.dat[1],'bid':self.dat[2],'ask':self.dat[3]}, index=[0])
                #self.queue.put(event.TickEvent(self.dftemp,self.dat[0].replace('/', '_')))
            else:
                break

            self.i+=1
            if self.i > 10000:
                break
            time.sleep(t)

    def disconnect(self):
        self.connected = False


if __name__ == '__main__':
    dataQ = Queue()
    td = TrueFXData(['EUR_USD'],dataQ)
    
