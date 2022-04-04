import dh as dh
import pandas as pd
from datetime import datetime
from pathlib import Path
import queue
import time

from newscatcher import Newscatcher
from newscatcher import describe_url
from newscatcher import urls

class NEWSData(object):
    def __init__(self):     #,env, pair, data, timeout=0, count=0
        self.bus_urls=urls(topic = 'business', language = 'en')
        
        

    def connect(self,t=0.5):
        for u in self.bus_urls:
            self.nc = Newscatcher(website = u, topic = 'business')
            self.nc.print_headlines()

    def disconnect(self):
        pass



#Allowed topics:
#`tech`, `news`, `business`, `science`, `finance`, `food`, 
#`politics`, `economics`, `travel`, `entertainment`, 
#`music`, `sport`, `world`

if __name__ == "__main__":
    nd=NEWSData()
    nd.connect()    