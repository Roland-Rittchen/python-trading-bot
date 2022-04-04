from abc import ABC, abstractmethod
import data.dh_oanda as OANDA
import data.dh_truefx as TFXD
import data.dh_records as REC

class DHFactory(object):
    #def __init__(self, env, pair, data):
    #    self.factory(env, pair, data)

    def factory(source, pairs, dQ):
        if source == 'oanda':
            return OANDA.OandaData(pairs, dQ)
        if source == 'truefx':
            return TFXD.TrueFXData(pairs, dQ) #env['queue'],pair,env['timerange'][0],env['timerange'][1])
        if source == 'records':
            return REC.RecordData(pairs, dQ) #env['queue'],pair,env['timerange'][0],env['timerange'][1])
    factory = staticmethod(factory)

    #def connect(self):
    #    pass
    

