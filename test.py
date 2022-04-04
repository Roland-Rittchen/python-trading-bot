import data.dh_truefx as TFXD
from multiprocessing import Queue

def test_dhtruefx():
    dataQ = Queue()
    td = TFXD.TrueFXData(['EUR_USD','GBP_USD'],dataQ)


def test_sample():
    #df=pd.DataFrame()
    pass

if __name__ == "__main__":
    test_dhtruefx()
    #test_sample()