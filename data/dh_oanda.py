import data.dh
import json
import pandas as pd
from oandapyV20 import API
from oandapyV20.exceptions import V20Error, StreamTerminated
from oandapyV20.endpoints.pricing import PricingStream
from oanda_auth import Auth
import event
from requests.exceptions import ConnectionError
import logging

logging.basicConfig(
    filename="v20.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
)

class OandaData(data.dh.DataHandler):

    def __init__ (self, env, pair, timeout=0, count=5): #queue, instruments=['EUR_USD'], timeout=0, count=0):
        self.queue=env.queue
        self.pair=pair
        self.instruments=[pair]

        accountID, access_token = Auth()
        # setup the stream request
        self.r=PricingStream(accountID=accountID, params={"instruments":",".join(self.instruments)})
        self.count=count
        self.request_params = {}
        
        if timeout !=0:
            self.request_params = {"timeout": timeout}

        self.api = API(access_token=access_token,
            environment="practice",
            request_params=self.request_params)

    def connect(self):
        self.n = 0
        while True:
            try:
                for self.R in self.api.request(self.r):
                    self.R = json.dumps(self.R, indent=2)
                    self.S = json.loads(self.R)
                    #print(self.S)
                    #print('\n')
                    if self.S["type"] == "PRICE":
                        self.dat={'time':self.S["time"].replace('T', ' ')[:-2],'bid':self.S["closeoutBid"], 'ask':self.S["closeoutAsk"]}
                        self.dftemp = pd.DataFrame({'time':self.dat['time'],'bid':self.dat['bid'],'ask':self.dat['ask']}, index=[0])
                        self.event=event.TickEvent(self.dftemp,self.pair)
                        
                        
                        self.queue.put(self.event)
                        self.n += 1
                        #print(str(self.n))
                    #if self.count != 0 and self.n >= self.count:
                        #self.r.terminate("self.counts received: {}".format(self.count))

            except V20Error as e:
                # catch API related errors that may occur
                with open("LOG", "a") as LOG:
                    LOG.write("V20Error: {}\n".format(e))
                break
            except ConnectionError as e:
                with open("LOG", "a") as LOG:
                    LOG.write("Error: {}\n".format(e))
            except StreamTerminated as e:
                with open("LOG", "a") as LOG:
                    LOG.write("Stopping: {}\n".format(e))
                break
            except Exception as e:
                with open("LOG", "a") as LOG:
                    LOG.write("??? : {}\n".format(e))
                break

    def disconnect(self):
        self.r.terminate("self.counts received: {}".format(self.count))

if __name__ == '__main__':
    dh = OandaData(['EUR_USD'],0,5)    #['EUR_USD'],0,5
    dh.connect()

"""
{
	'type': 'PRICE', 
	'time': '2020-05-26T12:28:20.063098670Z', 
	'bids': [
		{'price': '1.09675', 'liquidity': 1000000}, 
		{'price': '1.09674', 'liquidity': 2000000}, 
		{'price': '1.09673', 'liquidity': 2000000}, 
		{'price': '1.09671', 'liquidity': 5000000}], 
	'asks': [
		{'price': '1.09682', 'liquidity': 1000000}, 
		{'price': '1.09684', 'liquidity': 2000000}, 
		{'price': '1.09685', 'liquidity': 2000000}, 
		{'price': '1.09686', 'liquidity': 5000000}], 
	'closeoutBid': '1.09671', 
	'closeoutAsk': '1.09686', 
	'status': 'tradeable', 
	'tradeable': True, 
	'instrument': 'EUR_USD'
}
"""