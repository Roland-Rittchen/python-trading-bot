import datetime
import graph as graphics
import datahandler
import strategy.strat_1 as strat1
import records
import indicator_handler as indicator
import pandas as pd
import queue
import time
import timer
import logger
from multiprocessing import Process, Lock, Manager, Queue


class App(object):
    def __init__(self, env):
        self.env=env
        open('LOG', 'w').close()
        open('log.txt', 'w').close()

    def close(self):
        pass

    def dataCollector(self):
        pass
    '''
    def graphic(self, gQ):
        print('graphic starts here')
        #start a graph
        self.graph = graphics.Graph(gQ)
        self.graph.start()
    '''

    def main(self, dQ, dL): #t, , nspace
        i=0

        m = 0 #minute
        '''fm = 0 #5minute
        ftm = 0 #15minute
        tm = 0 #30minute
        hr = 0 #hour
        fhr = 0 #4hour
        d = 0 #day
        w = 0 #week
        mth = 0 #month
        yr = 0 #year'''

        while i<100000:
            try:
                event = dQ.get(False)
            except queue.Empty:
                pass
            else:
                if event is not None:
                    if event.type == 'TICK':
                        #vars(ns)[event.pair].append(event.data) #, ignore_index=False, verify_integrity=False, sort=False
                        #nspace.EUR_USD = nspace.EUR_USD.append(event.data, ignore_index=True)
                        for i in dL:
                            if self.env.inst_list[i] == event.pair:
                                #TICKDATA
                                dL[i][0].pop(0)
                                dL[i][0].append(event.data) #time, bid, ask, volume
                                #1 MINUTE OHLC
                                if event.data[0].minute > m or (m == 60 and event.data[0].minute < 60):
                                    m = event.data[0].minute
                                    dL[i][1]=[event.data[0],event.data[1],event.data[1],event.data[1]] #time, open, high, low, close
                                else:
                                    if event.data[1]>dL[i][1][-1][2]:
                                        dL[i][1][-1][2]=event.data[1]
                                    if event.data[1]<dL[i][1][-1][3]:
                                        dL[i][1][-1][3]=event.data[1]
                                    dL[i][1][-1][4]=event.data[1]    
                                break

                        if self.env.mode=='backtest':
                            self.env.timer.chkTimer(self.env, datetime.datetime.strptime(event.data['time'], '%Y-%m-%d %H:%M:%S.%f')) #event.data['time']
                        else:
                            self.env.timer.chkTimer(self.env,datetime.datetime.now(datetime.timezone.utc)) #event.data['time'],
                        for s in self.env.strategies:
                            s.onTick()
                    elif event.type == 'BAR':
                        pass

                    elif event.type == 'SIGNAL':
                        pass

                    elif event.type == 'ORDER':
                        pass

                    elif event.type == 'FILL':
                        pass

                    elif event.type == 'HOUR':
                        pass

                    elif event.type == 'DAY':
                        #update recorders
                        self.env.dailyUpdate()

                    elif event.type == 'WEEK':
                        pass

                    elif event.type == 'MONTH':
                        pass

                    elif event.type == 'YEAR':
                        pass
                    event.done()
                    self.env.logger.log_event(event.created, event.done)
                    #env['queue'].task_done()
            i+=1
            if dQ.qsize() == 0:
                time.sleep(0.5) #t


class Env(object): #environment of a session
    def __init__(self):
        #print('envinit')
        self.inst_list = ['EUR_USD'] #,'EUR_GBP','GBP_USD','EUR_GBP','GBP_USD'
        self.mode = 'record' #trade, backtest, record
        self.datasource = 'truefx' # "oanda", "truefx", "tickstory", "records"
        self.indicators = ['EMA'] #MACD
        self.timerange = ['2019_01','2019_01'] #timerange for the backtest if there is one
        self.datahandler = []
        self.strategies = [
            strat1.Strat()    
        ]
        #self.queue = queue.Queue()
        self.timer = timer.Timer()
        self.logger = logger.Logger()
        #for i in self.inst_list:
        #    print('ENV I')
        #    self.instruments.append(Inst(i, self, dataThreads))
        self.graphs=[[0,1]]

    def dailyUpdate(self):
        #for i in self.instruments:
        pass #i.newRec()


if __name__=='__main__':  
    print("INITIALIZE") 
    env = Env()

    dQueue = Queue()
    #gQueue = []

    gmgr = Manager()

    dList = gmgr.list() #time, bid, ask, volume
    #Data Collector List
    h=0
    for i in env.inst_list: #lvl1: Instruments
        dList.append(gmgr.list())
        for j in (range(0,11)): #lvl2: timeframe
            dList[h].append(gmgr.list())
            for k in (range(0,500)):    #lvl3: 500 lines of data each
                dList[h][j].append(gmgr.list([0,0,0,0])) #time, bid, ask, volume
        h+=1

    print(dList)

    a = App(env)
    G = graphics.Graph(env)

    print("START")

    dH = datahandler.DHFactory.factory(env.datasource, env.inst_list, dQueue)
    pdH = Process(target=dH.connect)
    pdH.start()

    pMain = Process(target=a.main,args=(dQueue, dList)) #[0.2], , ns
    pMain.start()

    pG = Process(target=G.start, args=(dList, ))
    pG.start()

    pdH.join()
    pMain.join()
    pG.join()