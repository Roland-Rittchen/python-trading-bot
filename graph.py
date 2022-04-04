import pandas as pd
import mplfinance as mpf
from datetime import datetime
import matplotlib.animation as animation
from multiprocessing import Queue
from queue import Empty
from talib.abstract import *

class Graph(object):

        def __init__(self, env):
                self.i=1
                self.grph=[]
                for i in env.graphs:
                        self.addInst(i)
                #print('GRAPH: '+str(id(self)))

        def addInst(self, inst):
                self.grph.append(Graphlet(self.i,inst))
                self.i+=1

        def remInst(self, inst):
                for g in self.grph:
                        if g.inst == inst:
                                #mpf.close(g.fignum)
                                pass

        def start(self, ns):
                for g in self.grph:
                        Graphlet.start(g, ns)
                mpf.show(block=True) #block = False
                
class Graphlet(Graph):

        def __init__(self, i, inst):
                self.fignum = i
                self.inst = inst[0]
                self.timef = inst[1]
                #self.data = pd.DataFrame(columns=['time','bid','ask'])
                #self.data.set_index('time')
                #self.fig = mpf.figure(style='charles',figsize=(7,8)) 
                #self.ax1 = self.fig.add_subplot(1,1,1)
                #self.ohlc=pd.DataFrame()

                self.ohlc= pd.DataFrame({'Date':datetime.now(),'open':1,'high':1,'low':1,'close':1}, index=[0])
                self.ohlc.set_index('Date')
                self.ohlc.index = pd.to_datetime(self.ohlc.index)

                self.exp12     = pd.DataFrame()
                self.exp26     = pd.DataFrame()
                self.macd      = pd.DataFrame()
                self.signal    = pd.DataFrame()
                self.histogram = pd.DataFrame()

                self.apds = [mpf.make_addplot(self.exp12,color='lime'),
                        mpf.make_addplot(self.exp26,color='c'),
                        mpf.make_addplot(self.histogram,type='bar',width=0.7,panel=1,
                                        color='dimgray',alpha=1,secondary_y=False),
                        mpf.make_addplot(self.macd,panel=1,color='fuchsia',secondary_y=True),
                        mpf.make_addplot(self.signal,panel=1,color='b',secondary_y=True),
                ]

                self.s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

                self.fig, self.axes = mpf.plot(self.ohlc,type='candle',addplot=self.apds,figscale=1.5,figratio=(7,5),title='\n\nMACD',
                                style=self.s,volume=False,panel_ratios=(6,3),returnfig=True)

                self.ax_main = self.axes[0]
                self.ax_emav = self.ax_main
                self.ax_hisg = self.axes[2]
                self.ax_macd = self.axes[3]
                self.ax_sign = self.ax_macd

        def animate(self, *fargs):
                self.evdata = self.dl[self.inst][self.timef] 

                #self.data=self.nspace.EUR_USD 
                #self.data=self.data.set_index('time')
                #self.data.index = pd.to_datetime(self.data.index)
                #self.data['bid'] = self.data['bid'].apply(pd.to_numeric, errors='coerce')
                #self.data['ask'] = self.data['ask'].apply(pd.to_numeric, errors='coerce')
                #self.ohlc=self.data['bid'].resample('5Min').ohlc()
                print(self.evdata)
                self.ohlc = pd.DataFrame(self.evdata)
                self.ohlc.columns = ['open', 'high', 'low', 'close']
                self.ohlc.index.name = "date"
                self.ohlc.index = pd.to_datetime(self.ohlc.index)
                #self.ohlc.rename(columns={"A": "a", "B": "c"})
                #print(self.ohlc)
                self.exp12 = EMA(self.ohlc, timeperiod=12)      #, price='Close'
                self.exp26 = EMA(self.ohlc, timeperiod=26)
                self.macd  = self.exp12 - self.exp26
                if self.macd.first_valid_index() != None:
                        self.signal = EMA(self.macd, timeperiod=9)
                else:
                        self.signal = self.exp12
                self.histogram = self.macd - self.signal

                self.apds = [mpf.make_addplot(self.exp12,color='lime',ax=self.ax_emav),
                        mpf.make_addplot(self.exp26,color='c',ax=self.ax_emav),
                        mpf.make_addplot(self.histogram,type='bar',width=0.7, color='dimgray',alpha=1,ax=self.ax_hisg),
                        mpf.make_addplot(self.macd,color='fuchsia',ax=self.ax_macd),
                        mpf.make_addplot(self.signal,color='b',ax=self.ax_sign),
                ]

                for ax in self.axes:
                        ax.clear()
                mpf.plot(self.ohlc,type='candle',addplot=self.apds,ax=self.ax_main)
                

        def start(self, dL):
                self.dl = dL
                self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=('5s'), interval=1000)